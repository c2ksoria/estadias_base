from django.shortcuts import render
from django.views.generic import ListView

from core.models import Commercial, Plan, Propietary
# CreateView, DetailView, UpdateView, TemplateView, DeleteView

# Create your views here.

def home(request):
    return render(request, 'base.html')


class PropietaryView(ListView):
    model=Propietary
    template_name: 'propietary.html'
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        print(queryset)
        queryset=queryset.filter(User=user)
        # print(queryset.User.username)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Datos del Propietario'
        user = self.request.user
        empresa_nombre=Propietary.objects.get(User=user.id)
        context['propietary']= empresa_nombre.User.username
        print(context)
        return context
    

class PlanView(ListView):
    model= Plan
    template_name: 'plan.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user = self.request.user
        empresa_nombre=Propietary.objects.get(User=user.id)
        context['propietary']= empresa_nombre.User.username
        planContratado=empresa_nombre.Plan
        context['plan']=planContratado
        context['titulo']= "Planes Disponibles"
        print("Plan Contratado............",planContratado)
        return context

class CommercialView(ListView):
     model=Commercial
     template_name: 'commercial.html'
     def get_queryset(self, *args, **kwargs):
         user = self.request.user
         queryset = super().get_queryset(*args, **kwargs)
         propietary_name=Propietary.objects.get(User=user.id)
         queryset = queryset.filter(User=propietary_name.id)
         return queryset
   
     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['titulo'] = 'Campañas Activas'
         user = self.request.user
         empresa_nombre=Propietary.objects.get(User=user.id)
         context['propietary']= empresa_nombre.Plan
         print("------------------")
         paqueteContratado=empresa_nombre.Plan
         print(paqueteContratado)
         commercialPayed=Commercial.objects.filter(User=empresa_nombre).count()
         campanaDisponibles=paqueteContratado.CommercialQty-commercialPayed
         context['campanaDisponibles']= campanaDisponibles
         return context