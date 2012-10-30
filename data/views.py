from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotAllowed, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.core.servers.basehttp import FileWrapper
from django.template.context import RequestContext

import time
import hashlib
import celery
import os

from data import tasks
from data.models import Files2taskId
from browse.modelspackage.sparql_local_wrapper import SparqlManager


def _unify_hash(l):
        return hashlib.md5(unicode(sorted(l))).hexdigest()

def _removeDataHostPrefix(url):
        return url.replace(settings.DATA_HOST_PREFIX, "")


@csrf_exempt
def download_redirect(request):
        # TODO: this is just a quick hack to show that this approach works, I'll
        # tidy it up if we decide to go this way
        if request.method == 'POST':
                """name=\w+&channel=<channel>&json={ 'media' : [<url>+], channels' : [<channel>+], 'name' : \w+ }"""
                try:
                        data = simplejson.loads(request.POST.get("json"))
                except ValueError:
                        return HttpResponseServerError("Malformed json object")

                if not 'media' in data:
                        return HttpResponseServerError('Invalid json query syntax - should be { "media" : [<url>+], "channels" : [<channel>+], "name" : "\w+" }')

                if not 'name' in data:
                        # we know how to handle an empty name
                        data['name'] = request.POST.get("name", "")

                channel = request.POST.get("channel")
                data['files'] = [ d for d in data['media'] if d.startswith(settings.DATA_HOST_PREFIX) ]
                if channel is not None:
                        s = SparqlManager()

                        q = """?item dc:isPartOf <%s> .
                ?item austalk:media ?media .
                ?media austalk:version 1 .
                ?media austalk:channel "%s" .
        """

                        qq = """select distinct ?media
where {
        {
                %s
        }
}
                        """ % " } UNION {\n\t\t".join(
                                        [ q % (d, channel) for d in data['media'] if not d.startswith(settings.DATA_HOST_PREFIX) ])
                        #print qq

                        files = s.query(qq)
                        data['files'] += [ f['media']['value'] for f in files['results']['bindings'] ]
               
                #print "Number of data file urls:", len(data['files'])

                urlPaths = map(_removeDataHostPrefix, data['files'])

                h = _unify_hash(urlPaths)
                try:
                        t = Files2taskId.objects.get(h=h)
                        # restart a failed job
                        res = celery.result.AsyncResult(t.task_id)
                        if res.failed():
                                res.forget()
                                t.delete()
                                raise Files2taskId.DoesNotExist

                except Files2taskId.DoesNotExist:
                        t = tasks.prepareDownload.apply_async((h, urlPaths), retry=False)
                        Files2taskId.objects.create(h=h, task_id=t.id)

                time.sleep(1.234)   # just to give the zip generation some time

                return HttpResponseRedirect(reverse("data:download", args=[h]) + "?name="+data['name'])
        else:
                return HttpResponseNotAllowed(['POST'])


def download(request, h):
        task = get_object_or_404(Files2taskId, h=h)
        res = celery.result.AsyncResult(task.task_id)

        name = request.GET.get("name", "")
        if len(name) == 0:
                name = "smallasc-search-data.zip"
        if not name.endswith(".zip"):
               name += ".zip"
        started_at = task.dt
        link = request.build_absolute_uri(request.get_full_path())

        if not res.ready():
            time.sleep(1.234)
            #response = HttpResponse("blablabla", status=307)
            #response['Location'] = reverse("download", kwargs={ 'h' : h })

            variables = RequestContext(request, {
                    'task_id' : task.task_id,
                    'started_at' : started_at,
                    'link' : link,
                    'name' : name,
            })

            return render_to_response("download-in-progress.html", variables)

        elif res.successful() and os.path.exists(os.path.join(settings.TEMP_ROOT, h+".zip")):
            wrapper = FileWrapper(file(os.path.join(settings.TEMP_ROOT, h+".zip")))
            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=%s' % name
            response['Content-Length'] = os.path.getsize(os.path.join(settings.TEMP_ROOT, h+".zip"))

            return response

        else: # res.failed():
            variables = RequestContext(request, {
                    'task_id' : task.task_id,
                    'started_at' : started_at,
                    'name' : name,
                    'link' : link,
                    'exception' : res.result,
                    'traceback' : res.traceback,
            })

            return render_to_response("download-failed.html", variables)

