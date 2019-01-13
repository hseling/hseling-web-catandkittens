from django.contrib import admin
from web.models import MetaFile, WordFile, CollocationFile


# Register your models here.

class MyAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(request)


admin.site.register(MetaFile, MyAdmin)
admin.site.register(WordFile, MyAdmin)
admin.site.register(CollocationFile, MyAdmin)
