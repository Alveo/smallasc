from django.http import HttpResponseRedirect
from django import forms

from django.contrib.auth.decorators import permission_required
from django.views.generic.list import ListView

from attachments.models import Attachment


# TODO: both list and upload views should be handled by the same view fn
# TODO: deal with uploading duplicate files - offer to replace

class UploadFileForm(forms.Form):
    file  = forms.FileField()
    description = forms.CharField()

@permission_required('attachments.add_attachment')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data['description']
            attachment = Attachment(file=request.FILES['file'], description=description, uploader=request.user)
            attachment.save()
            return HttpResponseRedirect('/attachments/')
    return HttpResponseRedirect('/attachments/')


class AttachmentListView(ListView):
    
    model = Attachment
    template_name = "list.html"