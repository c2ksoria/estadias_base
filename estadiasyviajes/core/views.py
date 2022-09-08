from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from core.models import Commercial, Plan, Propietary, CommercialPictures, Status
from core.form import AddImageCommercialForm, CreateFormCommercial, UpdateFormPropietary

from django.urls import reverse_lazy
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
        context['propietary']= getPropietary(self.request.user).User.username
        print(context)
        return context
    

class PlanView(ListView):
    model= Plan
    template_name: 'plan.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        propietary=getPropietary(self.request.user)
        context['propietary']= propietary.User.username
        planContratado=propietary.Plan
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
         propietary=getPropietary(self.request.user)
         context['propietary']= propietary.User.username
         print("------------------")
         paqueteContratado=propietary.Plan
         print(paqueteContratado)
         commercialPayed=Commercial.objects.filter(User=propietary).count()
         campanaDisponibles=paqueteContratado.CommercialQty-commercialPayed
         context['campanaDisponibles']= campanaDisponibles
         return context


# class CommercialUpdateView(UpdateView):
#     model=Commercial
#     form_class = UpdateFormCommercial
#     success_url ="/home/commercial"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = 'Editar Datos Multimedia'
#         user = self.request.user
#         empresa_nombre=Propietary.objects.get(User=user.id)
#         context['propietary']= empresa_nombre.Plan
#         print(context)
#         return context

class AddImageCommercialview(CreateView):
    model=CommercialPictures
    form_class= AddImageCommercialForm
    template_name= 'createCommercialImage.html'
    success_url=reverse_lazy('commercial')

    # def get_success_url(self, *args, **kwargs):
    #     return reverse_lazy('multimedia', args=[self.kwargs['pk']])

    def form_valid(self, form):
        id_Campana=self.kwargs['pk']
        print("------SLUG------")
        campana=Commercial.objects.get(id=id_Campana)
        
        form.instance.image = campana
        form.save()
        current_url = self.request
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['titulo']= 'Subir Imagen'
        user = self.request.user
        empresa_nombre=Propietary.objects.get(User=user.id)
        context['propietary']= empresa_nombre.Plan
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        print("------------Post------------")
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("Image")
        if form.is_valid():
            id_Campana=self.kwargs['pk']
            print("------SLUG------")
            comer=Commercial.objects.get(id=id_Campana)
            print("----------",comer)
            for f in files:
                print(f)
                CommercialPictures.objects.create(Commercial=comer,  Image=f, ResumeTextImage="holas")
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def AddCommercial(request):
    print("---------AddCommercial----------")
    print("Slug: ")
    form = CreateFormCommercial()
    
    print("USer: ",request.user.id)
    # suspended=Status.objects.get(id=2)
    # print(suspended)
    propietary= Propietary.objects.get(id=request.user.id)
    print(propietary)
    form = CreateFormCommercial()
    form.fields["User"].initial = 1
    # print(form)

    
    # form.Status=suspended
    
    if request.method == "POST":
        print(request.POST)
        form=CreateFormCommercial(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/home/commercial')
        else:
            print("----------------------Error!!!")
            print(form.errors)
            return redirect('/home/commercial')
            
    context={'form':form}
    context['propietary']= getPropietary(request.user).User.username
    return render(request, 'core/createCommercial.html', context)

def updateCommercial(request, pk):
    print("---------UpdateCommercial----------")
    print("Slug: ",pk)
    commercial= Commercial.objects.get(id=pk)
    print(commercial)
    form = CreateFormCommercial(instance=commercial)

    if request.method == "POST":
        print(request.POST)
        form=CreateFormCommercial(request.POST, instance=commercial)
        if form.is_valid():
            form.save()
            return redirect('/home/commercial')
            
    context={'form':form}
    context['propietary']= getPropietary(request.user).User.username
    return render(request, 'core/createCommercial.html', context)

class deleteCommercial(DeleteView):
    model = Commercial
    success_url = reverse_lazy('commercial')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # user = self.request.user
        # empresa_nombre=Propietary.objects.get(User=user.id)
        
        context['propietary']= getPropietary(self.request.user).User.username
        return context


def getPropietary(user):
    propietaryName=Propietary.objects.get(User=user.id)
    return propietaryName

def updatePropietary(request, pk):
    print("---------UpdateCommercial----------")
    print("Slug: ",pk)
    propietary= Propietary.objects.get(id=pk)
    print(propietary)
    form = UpdateFormPropietary(instance=propietary)
    # print (form)
    if request.method == "POST":
        form=UpdateFormPropietary(request.POST, instance=propietary)
        if form.is_valid():
            form.save()
            return redirect('/home/propietary')
            
    context={'form':form}
    context['propietary']= getPropietary(request.user).User.username

    return render(request, 'core/propietary_form.html', context)