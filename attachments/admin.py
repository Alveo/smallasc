from django.contrib import admin 
from attachments.models import Attachment
 
class AttachmentAdmin(admin.ModelAdmin):
   list_display = ['file', 'date', 'uploader']
   
admin.site.register(Attachment, AttachmentAdmin)
