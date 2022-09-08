from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import Commercial, CommercialPictures, Propietary

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
        # exclude = ('User', 'Status')
        
        widgets = {

            'CommercialName': forms.TextInput(attrs={'placeholder': 'Favor de ingresar un nombre Comercial'}),
            'ResumeText': forms.TextInput(attrs={'placeholder': 'Favor de introducir un texto breve que la actividad comercial'}),
            'CommercialAdress': forms.TextInput(attrs={'placeholder': 'Dirección Física Real'}),
            'CommercialEmail': forms.TextInput(attrs={'placeholder': 'Dirección Física Real'}),
        }
        labels = {
            'CommercialName': 'Nombre Comercial',
            'CommercialAdress': 'Dirección',
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
        widgets = {
            
        }
        labels = {
            'Status': 'Estado',
            'Plan' : 'Plan',
            'User': 'Usuario',
            'Image': 'Imagen',
            'BioPropietary': 'Bio'
        }

class UpdateFormPropietary(CreateFormPropietary):
    pass