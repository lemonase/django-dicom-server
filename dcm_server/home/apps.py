from django.apps import AppConfig
import os
import logging


logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    # custom hook for running code at django start
    def ready(self):
        run_once = os.environ.get("HOME_RUN_ONCE")
        if run_once is not None:
            return
        os.environ["HOME_RUN_ONCE"] = "True"

        print("Starting DICOM Store SCP server")

        from .models import DicomServer
        for server in DicomServer.objects.all():
            dicom_server = DicomServerRunner(
                server_name=server.hostname, port=server.port, ae_title=server.ae_title)
            dicom_server.run_server()


class DicomServerRunner:
    def __init__(self, server_name="DICOM C-STORE SCP Server",
                 addr="127.0.0.1", port=11112, ae_title="ANY-SCP"):
        self.server_name = server_name
        self.addr = addr
        self.port = port
        self.ae_title = ae_title

    def run_server(self):
        from pynetdicom._globals import ALL_TRANSFER_SYNTAXES
        from pynetdicom import (
            AE,
            evt,
            AllStoragePresentationContexts,
            VerificationPresentationContexts,
            debug_logger
        )

        transfer_syntax = ALL_TRANSFER_SYNTAXES[:]

        handlers = [
            (evt.EVT_C_ECHO, self.handle_echo),
            (evt.EVT_C_STORE, self.handle_store)
        ]

        # Initialise the Application Entity
        ae = AE(self.ae_title)

        # Support ALL storage transfer contexts
        for context in AllStoragePresentationContexts:
            ae.add_supported_context(context.abstract_syntax, transfer_syntax)

        # Support ALL verification contexts
        for context in VerificationPresentationContexts:
            ae.add_supported_context(context.abstract_syntax, transfer_syntax)

        print(
            f"{self.server_name} has been started at {self.addr}:{self.port} with AE Title: {self.ae_title}")

        # Start listening for incoming association requests
        ae.start_server((self.addr, self.port),
                        block=False, evt_handlers=handlers)

    def handle_echo(event):
        # requestor = event.assoc.requestor
        # timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        # msg = (
        #     "Received C-ECHO service request from ({}, {}) at {}"
        #     .format(requestor.address, requestor.port, timestamp)
        # )
        # logger.info(msg)

        return 0x0000

    # handle store testing: output_directory is temporary
    def handle_store(event, output_directory="~/scp_data/"):
        from pydicom.filewriter import write_file_meta_info
        from pydicom.dataset import Dataset
        from pydicom.uid import DeflatedExplicitVRLittleEndian
        from pynetdicom.dsutils import encode

        SOP_CLASS_PREFIXES = {
            "1.2.840.10008.5.1.4.1.1.2": ("CT", "CT Image Storage"),
            "1.2.840.10008.5.1.4.1.1.2.1": ("CTE", "Enhanced CT Image Storage"),
            "1.2.840.10008.5.1.4.1.1.4": ("MR", "MR Image Storage"),
            "1.2.840.10008.5.1.4.1.1.4.1": ("MRE", "Enhanced MR Image Storage"),
            "1.2.840.10008.5.1.4.1.1.128": ("PT", "Positron Emission Tomography Image Storage"),
            "1.2.840.10008.5.1.4.1.1.130": ("PTE", "Enhanced PET Image Storage"),
            "1.2.840.10008.5.1.4.1.1.481.1": ("RI", "RT Image Storage"),
            "1.2.840.10008.5.1.4.1.1.481.2": ("RD", "RT Dose Storage"),
            "1.2.840.10008.5.1.4.1.1.481.5": ("RP", "RT Plan Storage"),
            "1.2.840.10008.5.1.4.1.1.481.3": ("RS", "RT Structure Set Storage"),
            "1.2.840.10008.5.1.4.1.1.1": ("CR", "Computed Radiography Image Storage"),
            "1.2.840.10008.5.1.4.1.1.6.1": ("US", "Ultrasound Image Storage"),
            "1.2.840.10008.5.1.4.1.1.6.2": ("USE", "Enhanced US Volume Storage"),
            "1.2.840.10008.5.1.4.1.1.12.1": ("XA", "X-Ray Angiographic Image Storage"),
            "1.2.840.10008.5.1.4.1.1.12.1.1": ("XAE", "Enhanced XA Image Storage"),
            "1.2.840.10008.5.1.4.1.1.20": ("NM", "Nuclear Medicine Image Storage"),
            "1.2.840.10008.5.1.4.1.1.7": ("SC", "Secondary Capture Image Storage"),
        }

        try:
            ds = event.dataset
            # Remove any Group 0x0002 elements that may have been included
            ds = ds[0x00030000:]
        except Exception as exc:
            logger.error("Unable to decode the dataset")
            logger.exception(exc)
            # Unable to decode dataset
            return 0x210

        # Add the file meta information elements
        ds.file_meta = event.file_meta

        # Because pydicom uses deferred reads for its decoding, decoding errors
        #   are hidden until encountered by accessing a faulty element
        try:
            sop_class = ds.SOPClassUID
            sop_instance = ds.SOPInstanceUID
        except Exception as exc:
            logger.error(
                "Unable to decode the received dataset or missing 'SOP Class "
                "UID' and/or 'SOP Instance UID' elements"
            )
            logger.exception(exc)
            # Unable to decode dataset
            return 0xC210

        try:
            # Get the elements we need
            mode_prefix = SOP_CLASS_PREFIXES[sop_class][0]
        except KeyError:
            mode_prefix = "UN"

        filename = f"{mode_prefix}.{sop_instance}"
        logger.info(f"Storing DICOM file: {filename}")

        status_ds = Dataset()
        status_ds.Status = 0x0000

        # Try to save to output-directory
        if output_directory is not None:
            filename = os.path.join(output_directory, filename)
            try:
                os.makedirs(output_directory, exist_ok=True)
            except Exception as exc:
                logger.error("Unable to create the output directory:")
                logger.error(f"    {output_directory}")
                logger.exception(exc)
                # Failed - Out of Resources - IOError
                status_ds.Status = 0xA700
                return status_ds

        if os.path.exists(filename):
            logger.warning("DICOM file already exists, overwriting")

        try:
            if event.context.transfer_syntax == DeflatedExplicitVRLittleEndian:
                # Workaround for pydicom issue #1086
                with open(filename, "wb") as f:
                    f.write(b"\x00" * 128)
                    f.write(b"DICM")
                    write_file_meta_info(f, event.file_meta)
                    f.write(encode(ds, False, True, True))
            else:
                # We use `write_like_original=False` to ensure that a compliant
                #   File Meta Information Header is written
                ds.save_as(filename, write_like_original=False)

            status_ds.Status = 0x0000  # Success
        except IOError as exc:
            logger.error("Could not write file to specified directory:")
            logger.error(f"    {os.path.dirname(filename)}")
            logger.exception(exc)
            # Failed - Out of Resources - IOError
            status_ds.Status = 0xA700
        except Exception as exc:
            logger.error("Could not write file to specified directory:")
            logger.error(f"    {os.path.dirname(filename)}")
            logger.exception(exc)
            # Failed - Out of Resources - Miscellaneous error
            status_ds.Status = 0xA701

        return status_ds
