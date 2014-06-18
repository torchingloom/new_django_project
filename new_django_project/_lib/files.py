import os
import datetime
import hashlib

from django.conf import settings


def upload_file_location(folder=None, append_media_root=False, randomize_dirs=True):
    loc = folder
    if randomize_dirs:
        m = hashlib.md5()
        m.update(str(datetime.datetime.now()))
        m = m.hexdigest()
        loc = os.path.join(loc, m[:2], m[2:4], m[4:6])
    if append_media_root:
        loc = os.path.join(settings.MEDIA_ROOT, loc)
    return loc
