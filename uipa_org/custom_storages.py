from django.conf import settings
from django.core.files.storage import get_storage_class

from storages.backends.s3boto import S3BotoStorage


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally for compressor
    """
    location = settings.STATICFILES_LOCATION

    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
