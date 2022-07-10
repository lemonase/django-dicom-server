from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
        help_text="An AE Title for the DICOM server. The default is ANY-SCP"
    )
    ip_address = models.GenericIPAddressField(
        default="127.0.0.1",
        verbose_name="IP Address",
        help_text="IP Address of DICOM server (default is localhost 127.0.0.1)"
    )
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65536)],
        default=11112,
        verbose_name="Port Number"
    )
    is_running = models.BooleanField(default=False)

    class Meta:
        verbose_name = "DICOM Server"
        verbose_name_plural = "DICOM Servers"

    def __str__(self):
        return self.hostname