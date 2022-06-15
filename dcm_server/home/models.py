from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class DicomServer(models.Model):
    ae_title = models.CharField(unique=True, max_length=64)
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65536)])
    hostname = models.CharField(max_length=128)

    def __str__(self):
        return self.hostname
