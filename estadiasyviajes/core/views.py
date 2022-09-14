from dataclasses import field
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView

from core.models import Commercial, Plan, Propietary, CommercialPictures, Status, PropietarySocialNetworks, SocialNetworksNames
from core.form import AddImageCommercialForm, CreateFormCommercial, UpdateFormPropietary, UpdatePropietarySocialNetworks, updateFormPlanPropietary

from django.urls import reverse_lazy
from django.forms import inlineformset_factory

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
        context['id_propietary']= propietary

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
         context['titulo'] = 'Comercios Activos'
         propietary=getPropietary(self.request.user)
         context['propietary']= propietary.User.username
         print("------------------get_context_data")
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
    print("Slug: ",request.user.id)
    form = CreateFormCommercial()
    
    print("USer: ",request.user.id)
    # suspended=Status.objects.get(id=2)
    # print(suspended)
    slug=request.user.id
    propietary= Propietary.objects.get(id=slug)
    print(propietary)
    form = CreateFormCommercial(instance=propietary)
    # form.fields["User"].initial = slug
    # print(form)

    
    # form.Status=suspended
    
    if request.method == "POST":
        # print(request.POST)
        form=CreateFormCommercial(request.POST, instance=propietary)
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
    # print("Slug: ",pk)
    # commercial= Commercial.objects.get(id=pk)
    # print(commercial)
    # form = CreateFormCommercial(instance=commercial)

    # if request.method == "POST":
    #     print(request.POST)
    #     form=CreateFormCommercial(request.POST, instance=commercial)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/home/commercial')
            
    # context={'form':form}
    # context['propietary']= getPropietary(request.user).User.username
    # return render(request, 'core/createCommercial.html', context)
    SocialFormSet=inlineformset_factory(Propietary, PropietarySocialNetworks,UpdatePropietarySocialNetworks, fields={'PropietaryModel', 'SocialNetworksName', 'LinkSocialetwork'} , extra=0, can_delete = False)
    PropietaryModel= Propietary.objects.get(id=request.user.id)
    # print(PropietaryModel)
    commercial= Commercial.objects.get(id=pk)
    # print(commercial)
    propietaryForm=CreateFormCommercial(instance=commercial)
    # print(propietaryForm)
    print("-------------------------------------")
    Face_formset=SocialFormSet(instance=PropietaryModel)
    # print(Face_formset)
    # name=SocialNetworksNames.objects.all()
    if request.method == "POST":
        print("---------UpdateCommercial --->>>> POST ----------")
        # datos=request.POST
        # for item in datos:
        #     print(item)
        propietaryForm=CreateFormCommercial(request.POST,instance=commercial)
        Face_formset=SocialFormSet(request.POST, instance=PropietaryModel)
        print(Face_formset)
        if Face_formset.is_valid() and propietaryForm.is_valid():
            propietaryForm.save()
            Face_formset.save()
            print("----ALL forms are valid------")
            return redirect('/home/commercial')
        else:
            print("Error")
            # return redirect('/home/commercial')
            
    context={'propietaryForm': propietaryForm, 'Face_formset': Face_formset}
    # print (context)
    return render(request, 'core/updateCommercial.html', context)

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
    print("---------UpdatePropietary----------")
    print("Slug: ",pk)
    SocialFormSet=inlineformset_factory(Propietary, PropietarySocialNetworks,UpdatePropietarySocialNetworks, fields={'PropietaryModel', 'SocialNetworksName', 'LinkSocialetwork'} , extra=0, can_delete = False)
    PropietaryModel= Propietary.objects.get(id=pk)
    propietary= Propietary.objects.get(id=pk)
    propietaryForm=UpdateFormPropietary(instance=propietary)
    Formset=SocialFormSet( instance=PropietaryModel)

    if request.method == "POST":
        Formset=SocialFormSet(request.POST, instance=PropietaryModel)
        propietaryForm=UpdateFormPropietary(request.POST,instance=propietary)
        # form=UpdateFormPropietary(request.POST, instance=propietary)
        if Formset.is_valid() and propietaryForm.is_valid():
            Formset.save()
            propietaryForm.save()
            # context=super(updatePropietary).save()
            context={'saved': 'True'}
            return redirect('/home/propietary')
            
    context={'propietaryForm': propietaryForm, 'Formset': Formset}
    context['propietary']= getPropietary(request.user).User.username

    return render(request, 'core/propietary_form.html', context)

class testUpdate(TemplateView):
    template_name= 'core/testupdate.html'

    def get(self, request, *args, **kwargs):
        SocialFormSet=inlineformset_factory(Propietary, PropietarySocialNetworks,UpdatePropietarySocialNetworks, fields={'PropietaryModel', 'SocialNetworksName', 'LinkSocialetwork'} , extra=0, can_delete = False)
        PropietaryModel= Propietary.objects.get(id=kwargs['pk'])
        # print(PropietaryModel)
        propietaryForm=UpdatePropietarySocialNetworks(instance=PropietaryModel)
        print("-------------------------------------")
        Face_formset=SocialFormSet(instance=PropietaryModel)
        # print(Face_formset)
        name=SocialNetworksNames.objects.all()
        return self.render_to_response({ 'Face_formset': Face_formset, 'propietaryForm': propietaryForm})
        # # print(propietaryForm)
        # PropietaryModel=propietary
        # SocialForm=UpdatePropietarySocialNetworks(instance=PropietaryModel)
        # # print(SocialForm)
        # name= PropietarySocialNetworks.objects.all()
        # print (name)
        # facebook_name=name.filter(SocialNetworksName_id=4)
        # print (facebook_name)
        # print (name)
        # for item1 in name:
        #     print(item1.id)
        # new_instance=PropietarySocialNetworks()
        # new_instance.PropietaryModel=Propietary.objects.get(id=2)
        # new_instance.SocialNetworksName=SocialNetworksNames.objects.get(id=4)
        # print(new_instance)
        # new_instance.save()
    def post(self, request, *args, **kwargs):
        print("Entramos al post")

    def get_context_data(self, **kwargs):
        context=super(testUpdate,self).get_context_data(**kwargs)
        print("holasss")
        context['propietary']= getPropietary(self.request.user).User.username
        print(context)
        return context

class updatePlanPropietary(UpdateView):
    model=Propietary
    form_class = updateFormPlanPropietary
    template_name = 'core/update_plan.html'
    success_url = reverse_lazy('plan')
    extra_context = {'propietary': 'goalsdadls'}
  
    def get_context_data(self, **kwargs):
        context = super(updatePlanPropietary,self).get_context_data(**kwargs)
        context['titulo'] = 'Seleccionar el nuevo plan'
        context['propietary']= getPropietary(self.request.user).User.username
        print(context)
        return context