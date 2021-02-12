import os
from uuid import uuid4

from django.utils.deconstruct import deconstructible


@deconstructible
class UploadHexTo:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        return os.path.join(self.path, f'{uuid4().hex}.{ext}')
