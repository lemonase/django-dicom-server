class DicomServerRunner:
    def __init__(self, server_name="DICOM C-STORE SCP Server",
                 addr="127.0.0.1", port=11112, ae_title="STORESCP"):
        self.server_name = server_name
        self.addr = addr
        self.port = port
        self.ae_title = ae_title

    def run_server(self):
        from pynetdicom import AE, evt, AllStoragePresentationContexts, debug_logger
        handlers = [
            (evt.EVT_C_ECHO, self.handle_echo),
            (evt.EVT_C_STORE, self.handle_store)
        ]

        # Initialise the Application Entity
        ae = AE()

        # Support presentation contexts for all storage SOP Classes
        ae.supported_contexts = AllStoragePresentationContexts

        # Start listening for incoming association requests
        ae.start_server((self.addr, self.port),
                        block=True, evt_handlers=handlers)

        print("DICOM Server has been started!!")

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


# server_runner = DicomServerRunner()
# server_runner.run_server()
