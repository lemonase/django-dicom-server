from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class DicomServer(models.Model):
    hostname = models.CharField(
        unique=True, max_length=128, verbose_name="Hostname (friendly name)")
    ae_title = models.CharField(max_length=64, verbose_name="AE Title")
    ip_address = models.GenericIPAddressField(
        default="127.0.0.1",
        help_text="IP Address of DICOM server (default is localhost 127.0.0.1)",
        verbose_name="IP Address"
    )
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65536)],
        verbose_name="Port Number"
    )

    class Meta:
        verbose_name = "DICOM Server"
        verbose_name_plural = "DICOM Servers"

    def __str__(self):
        return self.hostname
