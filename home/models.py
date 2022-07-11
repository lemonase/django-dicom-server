from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import os


class DicomServer(models.Model):
    hostname = models.CharField(
        unique=True,
        max_length=128,
        verbose_name="Hostname (friendly name)",
        help_text="The hostname is just a friendly name used for identifying the server."
    )
    ae_title = models.CharField(
        max_length=64,
        default="ANY-SCP",
        verbose_name="AE Title",
        help_text="An AE Title for the DICOM server. The default is ANY-SCP."
    )
    ip_address = models.GenericIPAddressField(
        default="127.0.0.1",
        verbose_name="IP Address",
        help_text="The IP Address that this DICOM server will listen on (default is localhost 127.0.0.1)."
    )
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65536)],
        default=11112,
        verbose_name="Port Number",
        help_text="The port number that this DICOM Server will listen on (default is 11112)."
    )
    is_running = models.BooleanField(default=False)
    output_directory = models.CharField(
        max_length=255,
        default="djicom_output/output",
        help_text="The output directory where studies will be stored."
    )

    def get_output_files(self):
        return os.listdir(self.output_directory)

    def read_file_data(self, filename):
        with open(filename, "r") as file:
            return file.read()

    class Meta:
        verbose_name = "DICOM Server"
        verbose_name_plural = "DICOM Servers"

    def __str__(self):
        return self.hostname
