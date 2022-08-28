from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Status(models.Model):
    StatusName=models.CharField(max_length=50, verbose_name='Name')
    def __str__(self):
        return self.StatusName
    class Meta:
        verbose_name_plural = 'Status'

class Plan(models.Model):
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    PlanName=models.CharField(max_length=50, blank=False, verbose_name='Name')
    CommercialQty=models.IntegerField(blank=False, null=False,verbose_name='Commercial Quantity')
    AdviceQty=models.IntegerField(blank=False, null=False,verbose_name='Advice Quantity')
    CommercialImagesQty=models.IntegerField(blank=False, null=False,verbose_name='Commercial Images Quantity', default=0)
    CreationDate=models.DateField(auto_now=True, null=True)
    CreationTime=models.TimeField(auto_now=True, null=True)

    def __str__(self):
        return self.PlanName

        # Gastronomía
        # Estadías
        # Bares y Restaurantes
        # Discotecas
        # Experiencias
        # Excursiones
        # Gimnasios
        # Autos/Motos/Bicicletas
        # Movilidad (Remis, taxy, particulares)



class Propietary(models.Model):
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    Plan=models.ForeignKey(Plan, on_delete=models.SET_NULL,null=True,verbose_name='Plan')
    User=models.OneToOneField(User,on_delete=models.SET_NULL, max_length=50,null=True,verbose_name='User' )
    Image= models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.User.username

    class Meta:
        verbose_name_plural = 'Propietaries'

class Commercial(models.Model):
    User=models.OneToOneField(Propietary,on_delete=models.SET_NULL, max_length=50,null=True,verbose_name='User' )
    CommercialName=models.CharField(max_length=50, verbose_name='Name')
    lat = models.DecimalField(('Latitude'), max_digits=10, decimal_places=8)
    lng = models.DecimalField(('Longitude'), max_digits=11, decimal_places=8)
    phone_number = PhoneNumberField()
    CommercialEmail =models.EmailField(max_length = 254)

    def __str__(self):
        return self.CommercialName

    class Meta:
        verbose_name_plural = 'Commercial'

# class SocialNetworksNames(models.Model):
#     SocialNameNetwork=models.CharField(max_length=50, verbose_name='Name')
#     Commercial=models.ForeignKey(Commercial, on_delete=models.SET_NULL,verbose_name='Commercial')

#     def __str__(self):
#         return self.SocialNameNetwork

class SocialNetworksGlobal(models.Model):
    SocialName=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='SocialName')

    def __str__(self):
        return self.SocialName



class PropietaryPictures(models.Model):
    Image= models.ImageField(upload_to='images/province', null=True, blank=True)
    Propietary=models.ForeignKey(Propietary, on_delete=models.SET_NULL,null=True,verbose_name='Propietary')
    ResumeTextIamge=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    
    def __str__(self):
        return self.Propietary.User.username
    class Meta:
        verbose_name_plural = 'Propietary Pictures'

class Province(models.Model):
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    ProvinceName=models.CharField(max_length=50, verbose_name='ProvinceName')
    ResumeProvince=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    LongTextProvince=models.CharField(max_length=140, null=False, verbose_name='LargeText')
    def __str__(self):
        return self.ProvinceName

class ProvincePictures(models.Model):
    Image= models.ImageField(upload_to='images/province', null=True, blank=True)
    Province=models.ForeignKey(Province, on_delete=models.SET_NULL,null=True,verbose_name='Province')
    ResumeTextIamge=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    SubIndex=models.IntegerField(blank=False, null=False,verbose_name='Index Picture Order', default=0)
    
    def __str__(self):
        return self.Province.ProvinceName

    class Meta:
        verbose_name_plural = 'Province Pictures'



