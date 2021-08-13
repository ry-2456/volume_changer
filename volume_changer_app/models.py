from django.db import models
from .validator import FileValidator
from . import settings

class Music(models.Model):
    # file will be uploaded to MEDIA_ROOT/before_conversion/
    file = models.FileField(
            upload_to='before_conversion/',
            validators=[FileValidator( 
                max_size=settings.MAX_SIZE,
                content_types=settings.ALLOWED_CONTENT_TYPES)],
            )
    name = models.CharField(max_length=255)
