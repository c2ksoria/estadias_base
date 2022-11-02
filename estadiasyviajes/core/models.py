from datetime import datetime, timedelta
# from msilib.schema import Property
from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class Status(models.Model):
    StatusName=models.CharField(max_length=50, verbose_name='Name')
    def __str__(self):
        return self.StatusName
    class Meta:
        verbose_name_plural = 'Status'

class CommercialType(models.Model):
    NameCommercialType=models.CharField(max_length=140, null=False, verbose_name='Name Commercial Type')
    
    def __str__(self):
        return self.NameCommercialType

class Plan(models.Model):
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    PlanName=models.CharField(max_length=50, blank=False, verbose_name='Name')
    CommercialQty=models.IntegerField(blank=False, null=False,verbose_name='Commercial Qty')
    AdviceQty=models.IntegerField(blank=False, null=False,verbose_name='Advice Qty')
    CommercialImagesQty=models.IntegerField(blank=False, null=False,verbose_name='Images Qty', default=0)
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

class Province(models.Model):
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    ProvinceName=models.CharField(max_length=50, verbose_name='ProvinceName')
    TitleProvince=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    LongTextProvince=models.CharField(max_length=140, null=False, verbose_name='LargeText')
    def __str__(self):
        return self.ProvinceName

class Propietary(models.Model):
    Member=models.OneToOneField(User,on_delete=models.SET_NULL, max_length=50,null=True,verbose_name='User' )
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    Plan=models.ForeignKey(Plan, on_delete=models.SET_NULL,null=True,verbose_name='Plan')
    Image= models.ImageField(upload_to='images/', null=True, blank=True)
    BioPropietary=models.CharField(max_length=140, null=False, verbose_name='Biography', default="Sin Biografía por defecto")
    def __str__(self):
        return self.Member.username
    
    class Meta:
        verbose_name_plural = 'Propietaries'

@receiver(post_save, sender=Propietary)
def create_profile(sender, instance, created, **kwargs):
        if created:
            print("-----------Sobreescribiendo método de creación Propietary:....")
            name=SocialNetworksNames.objects.all()
            for item in name:
                print("-------Creando las redes sociales-------------")
                print(item.id)
                new_instance=PropietarySocialNetworks()
                new_instance.PropietaryModel=Propietary.objects.get(id=instance.id)
                new_instance.SocialNetworksName=SocialNetworksNames.objects.get(id=item.id)
                new_instance.save()

            print("-----------Saliendo de Sobreescribiendo método de escritura:....")


class AccommodationType(models.Model):
    AccommodationTypeName=models.CharField(max_length=140, null=False, verbose_name='Name Accommodation Type')
    # AccommodationTypeIcon=models.CharField(max_length=140, null=False, verbose_name='Link Icon Accommodation Type', default="Url empty")
    def __str__(self):
        return self.AccommodationTypeName
    class Meta:
        verbose_name_plural = 'Accommodation Type'

class Commercial(models.Model):
    User=models.ForeignKey(Propietary,on_delete=models.SET_NULL, max_length=50,null=True,verbose_name='User' )
    CommercialName=models.CharField(max_length=50, verbose_name='Name')
    CommercialAdress=models.CharField(max_length=50, verbose_name='Adress')
    ResumeText=models.CharField(max_length=140, verbose_name='Resume')
    Province=models.ForeignKey(Province, on_delete=models.SET_NULL,null=True,verbose_name='Province')
    lat = models.DecimalField(('Latitude'), max_digits=10, decimal_places=8)
    lng = models.DecimalField(('Longitude'), max_digits=11, decimal_places=8)
    phone_number = PhoneNumberField()
    CommercialEmail =models.EmailField(max_length = 254)
    CommercialType=models.ForeignKey(CommercialType, on_delete=models.SET_NULL,null=True,verbose_name='Accomodation')
    Status=models.ForeignKey(Status, on_delete=models.SET_NULL,null=True,verbose_name='Status')
    def __str__(self):
        return self.CommercialName

    class Meta:
        verbose_name_plural = 'Commercial'

class SocialNetworksNames(models.Model):
    SocialNetworkName=models.CharField(max_length=50, verbose_name='Name Social Network')
    def __str__(self):
        return self.SocialNetworkName
    class Meta:
        verbose_name_plural = "Social Network Name's"



class PropietarySocialNetworks(models.Model):
    PropietaryModel=models.ForeignKey(Propietary, on_delete=models.SET_NULL,null=True,verbose_name='Propietary')
    SocialNetworksName=models.ForeignKey(SocialNetworksNames, on_delete=models.SET_NULL,null=True,verbose_name='Social Network Name')
    LinkSocialetwork=models.CharField(max_length=140, null=False, verbose_name='Link Social Network', default="Url empty")
    def __str__(self):
        return self.PropietaryModel.User.username + "-" + self.SocialNetworksName.SocialNetworkName

class CommercialSocialNetworks(models.Model):
    CommercialModel=models.ForeignKey(Commercial, on_delete=models.SET_NULL,null=True,verbose_name='Propietary')
    SocialNetworksName=models.ForeignKey(SocialNetworksNames, on_delete=models.SET_NULL,null=True,verbose_name='Social Network Name')
    LinkSocialetwork=models.CharField(max_length=140, null=False, verbose_name='Link Social Network', default="Url empty")
    def __str__(self):
        return self.CommercialModel


class PropietaryPictures(models.Model):
    Image= models.ImageField(upload_to='images/propietary', null=True, blank=True)
    PropietaryImage=models.ForeignKey(Propietary, on_delete=models.SET_NULL,null=True,verbose_name='Propietary')
    ResumeTextIamge=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    
    def __str__(self):
        return self.PropietaryImage.User.username
    class Meta:
        verbose_name_plural = 'Propietary Pictures'

class ProvincePictures(models.Model):
    Image= models.ImageField(upload_to='images/province', null=True, blank=True)
    Province=models.ForeignKey(Province, on_delete=models.SET_NULL,null=True,verbose_name='Province')
    ResumeTextIamge=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    SubIndex=models.IntegerField(blank=False, null=False,verbose_name='Index Picture Order', default=0)
    
    def __str__(self):
        return self.Province.ProvinceName

    class Meta:
        verbose_name_plural = 'Province Pictures'

def calculo():
        now = datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start if start > now else start + timedelta(days=1)  


class Accommodation(models.Model):
    CommercialAccommodation=models.ForeignKey(Commercial, on_delete=models.SET_NULL,null=True,verbose_name='Commercial')
    NameCommercialAccomodation=models.CharField(max_length=140, null=False, verbose_name='Name', default="Example: Departamento 1")
    SmarTv=models.BooleanField(null=False, verbose_name='SmarTV', default=False)
    Microwave=models.BooleanField(null=False, verbose_name='Microwave', default=False)
    Oven=models.BooleanField(null=False, verbose_name='Oven', default=False)
    AirConditioning=models.BooleanField(null=False, verbose_name='Air Conditionning', default=False)
    Heating=models.BooleanField(null=False, verbose_name='Heating', default=False)
    Wifi=models.BooleanField(null=False, verbose_name='Wifi', default=False)
    garage=models.BooleanField(null=False, verbose_name='Garage', default=False)
    Rooms=models.IntegerField(blank=False, null=False,verbose_name='Rooms', default=0)
    SingleBed=models.IntegerField(blank=False, null=False,verbose_name='Single Bed', default=0)
    DoubleBed=models.IntegerField(blank=False, null=False,verbose_name='Double Bed', default=0)
    Crockery=models.BooleanField(blank=False, null=False,verbose_name='Crockery', default=0)
    CheckInTimeFrom=models.TimeField(null=False, default=calculo, verbose_name="Check In time from")
    CheckInTimeTo=models.TimeField(null=False, default=calculo, verbose_name="Check In time to")
    CheckOutTimeFrom=models.TimeField(null=False, default=calculo, verbose_name="Check Out time from")
    CheckOutTimeTo=models.TimeField(null=False, default=calculo, verbose_name="Check Out time to")
    def __str__(self):
        return self.NameCommercialAccomodation

    # class Meta:
    #     verbose_name_plural = 'Province Pictures'


class CommercialPictures(models.Model):
    Image= models.ImageField(upload_to='images/commercial', null=True, blank=True)
    Commercial=models.ForeignKey(Commercial, on_delete=models.SET_NULL,null=True,verbose_name='Commercial')
    ResumeTextImage=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    SubIndex=models.IntegerField(blank=False, null=True,verbose_name='Index Picture Order', default=0)
    
    def __str__(self):
        return self.ResumeTextImage
    class Meta:
        verbose_name_plural = 'Commercial Pictures'

class AccomodationPictures(models.Model):
    Image= models.ImageField(upload_to='images/commercial', null=True, blank=True)
    Accommodation=models.ForeignKey(Accommodation, on_delete=models.SET_NULL,null=True,verbose_name='Accommodation')
    ResumeTextImage=models.CharField(max_length=140, null=False, verbose_name='ResumeText')
    SubIndex=models.IntegerField(blank=False, null=False,verbose_name='Index Picture Order', default=0)
    
    def __str__(self):
        return self.Accommodation.NameCommercialAccomodation
    class Meta:
        verbose_name_plural = 'Accomodation Pictures'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            # email=self.normalize_email(email),
        )
        print("------------User Created-------")
        # user.set_password(password)
        user.save(using=self._db)
        return user