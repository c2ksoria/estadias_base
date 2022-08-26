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

class Commercial(models.Model):
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

class Propietary(models.Model):
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    User=models.OneToOneField(User,on_delete=models.SET_NULL, max_length=50,null=True,verbose_name='User' )
    Image= models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.User

    class Meta:
        verbose_name_plural = 'Propietaries'


