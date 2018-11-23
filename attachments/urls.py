from django.conf.urls import url
from attachments.views import  AttachmentListView,upload_file,delete_file

urlpatterns = [
    url (r'^$', AttachmentListView.as_view(), name="attachments"),
    url (r'^delete/', delete_file, name="delete_file"),
    url (r'^upload/', upload_file, name="upload_file"),
]
