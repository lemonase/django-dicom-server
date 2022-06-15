from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    # custom hook for running code at django start
    def ready(self):
        print("Starting DICOM Store SCP server")
        # logger.info("Starting DICOM Store SCP server")
        # pynetdicomsrv()


# TODO: move this into a separate module, maybe a separate namespace
def pynetdicomsrv():
    from pynetdicom import AE, evt, AllStoragePresentationContexts, debug_logger

    debug_logger()

    def handle_echo(event):
        requestor = event.assoc.requestor
        timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        msg = (
            "Received C-ECHO service request from ({}, {}) at {}"
            .format(requestor.address, requestor.port, timestamp)
        )
        logger.info(msg)

        return 0x0000

    def handle_store(event):
        """Handle a C-STORE request event."""
        # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
        ds = event.dataset

        # Add the File Meta Information
        ds.file_meta = event.file_meta

        # Save the dataset using the SOP Instance UID as the filename
        ds.save_as(ds.SOPInstanceUID, write_like_original=False)

        # Return a 'Success' status
        return 0x0000

    handlers = [
        (evt.EVT_C_ECHO, handle_echo),
        (evt.EVT_C_STORE, handle_store)
    ]

    # Initialise the Application Entity
    ae = AE()

    # Support presentation contexts for all storage SOP Classes
    ae.supported_contexts = AllStoragePresentationContexts

    # Start listening for incoming association requests
    ae.start_server(("127.0.0.1", 11112), blocking=False,
                    evt_handlers=handlers)
