from pynetdicom import AE, VerificationPresentationContexts

ae = AE(ae_title='MY_ECHO_SCP')

ae.supported_contexts = VerificationPresentationContexts

ae.start_server(("localhost", 11112), block=True)
