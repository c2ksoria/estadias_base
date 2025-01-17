from dataclasses import field
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView

from core.models import Commercial, Plan, Propietary, CommercialPictures, Status, PropietarySocialNetworks, SocialNetworksNames, Accommodation, AccomodationPictures
from core.form import AddImageCommercialForm, CreateFormCommercial, UpdateFormPropietary, UpdatePropietarySocialNetworks, updateFormPlanPropietary, CreateAccommodation, CreatePictureAccomodation, CreateFormPropietary

from django.urls import reverse_lazy, reverse
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
        queryset=queryset.filter(Member=user)
        # print(queryset.User.username)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Datos del Propietario'
        context['propietary']= getPropietary(self.request.user).Member.username
        print(context)
        return context
    

class PlanView(ListView):
    model= Plan
    template_name: 'plan.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        propietary=getPropietary(self.request.user)
        context['propietary']= propietary.Member.username
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
         propietary_name=Propietary.objects.get(Member=user.id)
         queryset = queryset.filter(User=propietary_name.id)
         return queryset
   
     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['titulo'] = 'Comercios Activos'
         propietary=getPropietary(self.request.user)
         context['propietary']= propietary.Member.username
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
        form=CreateFormCommercial(request.POST)
        form.instance.User=propietary
        print(form)
        if form.is_valid():
            print("---------El formulario es válido----------")
            form.save()
            return redirect('/home/commercial')
        else:
            print("----------------------Error!!!")
            print(form.errors)
            return redirect('/home/commercial')
            
    context={'form':form}
    context['propietary']= getPropietary(request.user).Member.username
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
    # context['propietary']= getPropietary(request.user).Member.username
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
    context['propietary']= getPropietary(request.user).Member.username
    # print (context)
    return render(request, 'core/updateCommercial.html', context)

class deleteCommercial(DeleteView):
    model = Commercial
    success_url = reverse_lazy('commercial')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # user = self.request.user
        # empresa_nombre=Propietary.objects.get(User=user.id)
        
        context['propietary']= getPropietary(self.request.user).Member.username
        return context


def getPropietary(user):
    propietaryName=Propietary.objects.get(Member=user.id)
    return propietaryName


def updatePropietary(request, pk):
    print("---------UpdatePropietary----------")
    propietaryData=Propietary.objects.get(id=pk)
    form = CreateFormPropietary(instance=propietaryData)
    
    if request.method == "POST":
        form = CreateFormPropietary(request.POST, request.FILES, instance=propietaryData)
        for item in form:
            print(form)
        
        if form.is_valid():
            form.save()
            
            return redirect('/home/propietary')
    
    context={'form': form}
    context['propietary']= getPropietary(request.user).Member.username

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
        context['propietary']= getPropietary(self.request.user).Member.username
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
        context['propietary']= getPropietary(self.request.user).Member.username
        print(context)
        return context

class AccomodationCommercialList(ListView):
    model=Accommodation
    template_name: 'accommodation_list.html'
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)
        
        commercial=Commercial.objects.get(id=user.id)
        print (commercial)
        print(queryset)
        self.commercial= commercial
        pk=self.kwargs['pk']
        queryset=queryset.filter(CommercialAccommodation= pk)
        # print(queryset.User.username)
        return queryset
    
    def get_context_data(self, **kwargs):
        print("------------------get_context_data")
        context = super().get_context_data(**kwargs)
        commercial_1=Commercial.objects.get(id=self.kwargs['pk'])
        context['titulo'] = 'Listado de Hospedajes de '+ " " + commercial_1.CommercialName
        context['propietary']= getPropietary(self.request.user).Member.username
        propietary=getPropietary(self.request.user)
        paqueteContratado=propietary.Plan
        print(paqueteContratado)
        commercialPayed=Commercial.objects.filter(User=propietary).count()
        campanaDisponibles=paqueteContratado.CommercialQty-commercialPayed
        context['campanaDisponibles']= campanaDisponibles
        context['pk']=self.kwargs['pk']
        
        return context

def newCommercialAccommodationList(request, pk):
    print("-------------PK---------",pk)
    propietary=getPropietary(request.user)
    paqueteContratado=propietary.Plan
    commercial=Commercial.objects.filter(User=propietary)
    commercialUsed=0
    # en commercialUser sumar los demás tipos de comercios; tales como gastronomía
    for item in commercial:
        commercialUsed+=Accommodation.objects.filter(CommercialAccommodation=item).count()
    adsAviables=paqueteContratado.AdviceQty-commercialUsed
    CommercialAccommodationId=Commercial.objects.get(id=pk)
    object_list=Accommodation.objects.filter(CommercialAccommodation=CommercialAccommodationId)
    context={'listado':object_list}
    context['pk']=pk
    context['titulo'] = 'Listado de Hospedajes de '+ " " + CommercialAccommodationId.CommercialName
    context['propietary']= propietary.Member.username

    context['adsAviables']= adsAviables
    return render(request, 'core/accommodation_list.html', context)

class AccommodationCommercialAdd(CreateView):
    model=Accommodation
    form_class=CreateAccommodation
    # success_url=reverse_lazy('commercial')
    
    def form_valid(self, form):
        print("--------------------------------------")
        user = self.request.user
        commercialId=self.kwargs['pk']
        print(commercialId)
        print("--------------------------------------")
        propietary=Commercial.objects.get(id=commercialId)
        print(propietary)
        print("--------------------------------------")

        # commercial=Commercial.objects.get(User=commercialId)
        form.instance.CommercialAccommodation = propietary
        # print(form)
        self.data_id=commercialId
        form.save()
        # current_url = self.request
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Agregar un Aviso'
        context['propietary']= getPropietary(self.request.user).Member.username
        print(context)
        commercialId=self.kwargs['pk']
        context['data_id']=commercialId
        return context
    def get_success_url(self):
        # print("--------------get_success_url------------")
        # print(self.data_id)
        # print("--------------------------------------")

        # return HttpResponseRedirect(reverse_lazy(newCommercialAccommodationList, kwargs={'pk': pk}))
        return reverse('newCommercialAccommodationList', kwargs={'pk': self.data_id})


class deleteAccommodation(DeleteView):
    model = Accommodation
    
    def get_object(self, queryset=None):
        print('-----------------deleteAccommodation-----------------------------')
        # obj = super(Accommodation, self).get_object()
        # print(obj)
        # print(self.kwargs)
        # print(self.kwargs['id_hospedaje'], self.kwargs['pk1'])
        Id=self.kwargs['id_hospedaje']
        # object_instance = Accommodation.objects.filter(id=Id)

        
        return self.get_queryset().filter(pk=Id).get()
        

    def get_success_url(self, *args, **kwargs):
        # Assuming there is a ForeignKey from Comment to Post in your model
        print("-----------_get_success_url-------")
        # post = self.object.post
        # print(post)
        pk1=self.kwargs['pk1']

        return reverse_lazy('AccomodationCommercialList', kwargs={'pk': pk1})





    def get_context_data(self, *args, **kwargs):
        print('-------get_context_data---------')
        context = super().get_context_data(**kwargs)
        for item in context:
            print(item)
        # print(type(context['accommodation']))
        Id=self.kwargs['id_hospedaje']
        pk1=self.kwargs['pk1']
        context['pk1']=pk1
        context['id_hospedaje']=Id

        # print(Id, pk1)
        return context

def newUpdateAccommodation(request, pk, pk1):
    CommercialId= Commercial.objects.get(id=pk)
    AccomodationData= Accommodation.objects.get(id=pk1)
    form=CreateAccommodation(instance=AccomodationData)

    context={'form': form}
    context['pk']=pk
    context['pk1']=pk1
    
    if request.method == "POST":
        form=CreateAccommodation(request.POST, instance=AccomodationData)
        if form.is_valid():

            accomodationUpdate=form.save()
            return HttpResponseRedirect(reverse_lazy(newCommercialAccommodationList, kwargs={'pk': pk}))
        else:
            print("--------------Error-----------")
            return redirect('/home/commercial')
    context['update']= True

    return render(request,'core/accommodation_form.html',context)

class AccommodationUpdate(UpdateView):
    template_name: 'core/accommodation_form.html'
    model=Accommodation
    form_class = CreateAccommodation
    # success_url = 'home/propietary'
    # def get_queryset(self, *args, **kwargs):
    #     print("------------get_queryset--------")
    #     queryset = super(AccommodationUpdate, self).get_queryset()
    #     filtro=queryset.filter(id=self.kwargs['pk'])
    #     print("filtro: ", filtro)
    #     return filtro

    def get(self, request, *args, **kwargs):
        print("----------get--------")
        print(self.kwargs['pk'],self.kwargs['pk1'])
        self.object = self.get_object()
        # print(self.object)
        return super().get(request, *args, **kwargs)

    # def form_valid(self, form):
    #     print("----------------AccommodationUpdate----------------------")
    #     user = self.request.user
    #     commercialId=self.kwargs['pk']
    #     print(commercialId)
    #     print("--------------------------------------")
    #     propietary=Accommodation.objects.get(id=commercialId)
    #     print(propietary.NameCommercialAccomodation, propietary.CommercialAccommodation)
    #     print("--------------------------------------")

    #     # commercial=Commercial.objects.get(User=commercialId)
    #     form.instance.CommercialAccommodation = propietary.CommercialAccommodation
    #     # print(form)
    #     self.data_id=commercialId
    #     form.save()
    #     # current_url = self.request
    #     return super().form_valid(form)
    def get_context_data(self, **kwargs):
        print("-----------get_context_data----------")
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Datos de Hospedaje'
        commercialId=self.kwargs['pk1']
        context['pk1']=commercialId
        context['pk']=self.kwargs['pk']
        context['update']= True
        # print(context)
        return context
    # def get_success_url(self):
    #     # print("--------------get_success_url------------")
    #     # print(self.data_id)
    #     # print("--------------------------------------"           # Aquí hay que arreglar el reverso para que vuelva a la pantalla que corresponde
    #     return reverse('AccomodationCommercialList', kwargs={'pk': 27})


def AccomodationPicturesView(request, pk):
    print("---------AccomodationPicturesView----------")
    print("Slug: ",pk)
    
    # images= AccomodationPictures.objects.get(id=pk)
    
    print("----------------------AccommodatioId----------------------")
    AccommodationId= Accommodation.objects.get(id=pk)
    print(AccommodationId)
    images= AccomodationPictures.objects.filter(Accommodation=AccommodationId)
    form = CreatePictureAccomodation(initial={'Accommodation':AccommodationId})
    
    # form.initial.Accommodation=AccommodationId
    print("-----------------Form------------")
    print(form)
    # for item in images:
    #     print(item.Image)

    context={'form': form}
    context['images']= images
    context['pk']=pk
    context['propietary']= getPropietary(request.user).Member.username
    print(getPropietary(request.user).User.username)

    if request.method == "POST":
        # print(request.POST)
        form = CreatePictureAccomodation(request.POST, request.FILES)
        form.instance.Accommodation=AccommodationId
        print("-----------------Form from POST!! ------------")
        print(form)

        if form.is_valid():
            print("------Form is valid!!!")
            form.save()            
            render(request, 'core/image_accommodation_form.html', context)
            
        else:
            print("Error!")
    
    return render(request, 'core/image_accommodation_form.html', context)

    

def test(request,pk1,pk2):
    
    print(pk1, pk2)
    return reverse_lazy(AccomodationCommercialList, kwargs={'pk': 1})