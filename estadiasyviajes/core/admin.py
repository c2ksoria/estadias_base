from django.contrib import admin
from .models import *

# Register your models here.
# class PropietaryAdmin(admin.ModelAdmin):
#     list_display=('id','User')
#     search_fields=('id','User')
    # list_filter = ('NombreEmpresa','CuitEmpresa')


admin.site.register(Propietary)
admin.site.register(Status)
admin.site.register(Commercial)
