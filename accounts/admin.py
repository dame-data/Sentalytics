from django.contrib import admin
from accounts.models import FileUploads
# Register your models here.
class FileUploadAdmin(admin.ModelAdmin):
	list_display = ('user','title','summary','created_at')
	search_fields = ('created_at','title')

admin.site.register(FileUploads,FileUploadAdmin)
