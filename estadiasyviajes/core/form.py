from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import Commercial, CommercialPictures, Propietary, PropietarySocialNetworks, Accommodation

# class CreateFormCampana(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for form in self.visible_fields():
#             form.field.widget.attrs['class']="form-control"
#     class Meta:
#         model = Campana
#         fields='__all__'
#         exclude = ('empresa',)

# class UpdateFormCampana(CreateFormCampana):
#     pass
        

class CreateFormCommercial(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"
    class Meta:
        model = Commercial
        fields='__all__'
        exclude = ('User', 'Status')
        widgets = {

            'CommercialName': forms.TextInput(attrs={'placeholder': 'Favor de ingresar un nombre Comercial'}),
            'ResumeText': forms.TextInput(attrs={'placeholder': 'Favor de introducir un texto breve que la actividad comercial'}),
            'CommercialAdress': forms.TextInput(attrs={'placeholder': 'Dirección Física Real'}),
            'CommercialEmail': forms.TextInput(attrs={'placeholder': 'Dirección Física Real'}),
            'ResumeText': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'CommercialName': 'Nombre Comercial',
            'CommercialAdress': 'Dirección',
            'ResumeText': 'Resumen',
            'Province': 'Provincia',
            'CommercialEmail': 'Teléfono',
            'Province': 'Provincia',
            'phone_number': 'Número de Teléfono',
            'CommercialEmail': 'Email',
            'CommercialType': 'Rubro',
            'lat': 'Latitud',
            'lng': 'Longitud',

        }



class UpdateFormCommercial(CreateFormCommercial):
    pass

class AddImageCommercialForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"
    
    class Meta:
        model = Commercial
        fields='__all__'
        widgets = {
            'Image': forms.ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            'Image': 'Imagen',
            'ResumeTextImage': 'Texto de Imagen',
            'SubIndex': 'Orden',
        }

class CreateFormPropietary(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"
    
    class Meta:
        model = Propietary
        fields='__all__'
        exclude = ('Status',)
        widgets = {

            'BioPropietary': forms.Textarea(attrs={'rows': 3}),
 
        }
        labels = {
            'Nombre': 'Estado',
            'Plan' : 'Plan',
            'User': 'Usuario',
            'Image': 'Imagen',
            'BioPropietary': 'Bio'
        }

class UpdateFormPropietary(CreateFormPropietary):
    pass

class CreatePropietarySocialNetworks(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"
    
    class Meta:
        model = PropietarySocialNetworks
        fields='__all__'
        widgets = {
            'SocialNetworksName':  forms.Select(attrs={'disabled': 'True'}),
        }
        labels = {
            'PropietaryModel': 'Propietario',
            'SocialNetworksName' : 'Nombre de Red Social',
            'LinkSocialetwork': 'link',
        }

class UpdatePropietarySocialNetworks(CreatePropietarySocialNetworks):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"
    pass
    class Meta:
        model = PropietarySocialNetworks
        fields='__all__'
        exclude = ('PropietaryModel',)
        widgets = {
            # 'SocialNetworksName':  forms.Select(attrs={'disabled': 'True'}),
        }
        

class updateFormPlanPropietary(CreateFormPropietary):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"
    class Meta:
        model = Propietary
        fields='__all__'
        exclude = ('Status', 'User', 'Image', 'BioPropietary',)
        widgets = {
            
        }
        labels = {
            'Plan' : 'Plan'
        }

class CreateAccommodation(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class']="form-control"
    
    class Meta:
        model = Accommodation
        fields='__all__'
        # widgets = {
        #     'SocialNetworksName':  forms.Select(attrs={'disabled': 'True'}),
        # }
        exclude={'CommercialAccommodation'}
        labels = {
             'NameCommercialAccomodation': 'Nombre',
             'Microwave' : 'Microondas',
             'Oven': 'Horno',
             'AirConditioning': 'Aire Acondicionado',
             'Heating':'Calefacción',
             'garage':'Estacionamiento',
             'Rooms':'Habitaciones',
             'SingleBed':'Camas Simples',
             'DoubleBed':'Camas Dobles',
             'Crockery':'Valijja',
             'CheckInTimeFrom':'Checkin desde',
             'CheckInTimeTo':'Checkin hasta',
             'CheckOutTimeFrom':'Checkout desde',
             'CheckOutTimeTo':'Checkout hasta',

         }
