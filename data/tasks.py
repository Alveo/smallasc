from django.conf import settings
from django.core.mail import mail_admins

from data.models import Files2taskId

from celery import task
from celery.decorators import periodic_task
import celery

import zipfile
from StringIO import StringIO
import os
import sys
import datetime

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


@periodic_task(run_every=datetime.timedelta(minutes=123))
def cleanFailedAndStaleTasks():
        cleaned = []

        for task in Files2taskId.objects.all():
                res = celery.result.AsyncResult(task.task_id)

                if res.failed() or (not res.ready() and now - dt > settings.TASK_TIMEOUT):
                        cleaned.append((res.result, res.traceback, task.dt, res.failed()))
                        if os.path.isfile(os.path.join(settings.TEMP_ROOT, "%s.zip" % task.h)):
                                        os.unlink(os.path.join(settings.TEMP_ROOT, "%s.zip" % task.h))
                        res.forget()
                        task.delete()

        if len(cleaned) > 0:
                msg = """Oops, some jobs had to be killed because they either failed or did not finish in time.

%s

Cheers,
Yours cleanFailedAndStaleTasks()
""" % "\n".join("Start: %s,\nResult: %s,\nStatus: %s,\nTraceback: %s\n" % \
                                (unicode(job[2]), unicode(job[0]), job[3] and "FAILED" or "TIMEOUT", job[1]) 
                                                                                for job in cleaned)
                mail_admins("Oops, some jobs had to be killed", msg, fail_silently=True)


@periodic_task(run_every=datetime.timedelta(minutes=33))
def maintainZipTempStorageSize():
        files = Files2taskId.objects.all().order_by("dt")
        # just to make sure somebody didn't delete the file manually
        successFiles =  [ f for f in files if celery.result.AsyncResult(f.task_id).successful() and \
                                        os.path.isfile(os.path.join(settings.TEMP_ROOT, "%s.zip" % f.h)) ]
        size = sum( os.path.getsize(os.path.join(settings.TEMP_ROOT, "%s.zip" % f.h)) for f in successFiles)

        oldSize = size
        oldCount = len(successFiles)
        count = oldCount

        sys.stderr.write("%d %d\n" % (int(size / 1024 / 1024), count))
        if size > settings.TEMP_ROOT_MAX * 1024 * 1024:     # in MB
                # delete the oldest jobs/zip files
                for f in successFiles:
                        size -= os.path.getsize(os.path.join(settings.TEMP_ROOT, "%s.zip" % f.h))
                        count -= 1

                        os.unlink(os.path.join(settings.TEMP_ROOT, "%s.zip" % f.h))
                        f.delete()
                        if size <= settings.TEMP_ROOT_MIN * 1024 * 1024:  # in MB
                                break

                msg = """The oldest zip files have been removed because the storage quota has been reached.

Old storage size: %d MB
Old number of zip files: %d

New storage size: %d MB
New number of zip files: %d

Cheers,
Yours maintainZipTempStorageSize()
                """ % (int(oldSize /1024/1024), oldCount, int(size/1024/1024), count)

                mail_admins("Removed old zip files", msg, fail_silently=True)


