from django.conf import settings

from celery import task
import zipfile
from StringIO import StringIO
import os
import sys

@task()
def add(x, y):
            """Sample django celery task"""
            return x + y


@task()
def prepareDownload(h, l):
            archive = zipfile.ZipFile(os.path.join(settings.TEMP_ROOT, h+".zip"), 'w', zipfile.ZIP_DEFLATED)
            notFound = StringIO()
            for f in l:
                    fp = os.path.join(settings.DATA_ROOT, f)
                    if os.path.exists(fp):
                            archive.write(fp, f)
                    else:
                            notFound.write(fp + "\n")
            notFound.seek(0)
            notFoundStr = notFound.read()
            if len(notFoundStr):
                    archive.writestr("not-found.txt", notFoundStr)
            archive.close()

