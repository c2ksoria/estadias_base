from django.contrib import admin
from .models import *

# Register your models here.
# class PropietaryAdmin(admin.ModelAdmin):
#     list_display=('id','User')
#     search_fields=('id','User')
    # list_filter = ('NombreEmpresa','CuitEmpresa')


class PlanAdmin(admin.ModelAdmin):
    list_display=('id','PlanName','CommercialQty', 'AdviceQty', 'CommercialImagesQty')
    search_fields=('id','CommercialQty')


admin.site.register(Propietary)
admin.site.register(Status)
admin.site.register(Commercial)
admin.site.register(Province)
admin.site.register(SocialNetworksNames)
admin.site.register(CommercialType)
admin.site.register(Accommodation)
admin.site.register(AccommodationType)
admin.site.register(ProvincePictures)
admin.site.register(CommercialPictures)
admin.site.register(PropietaryPictures)
admin.site.register(AccomodationPictures)
admin.site.register(Plan, PlanAdmin)
