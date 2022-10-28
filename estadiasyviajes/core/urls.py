from django.contrib import admin
from django.urls import path, include
from .views import  AccommodationUpdate, CommercialView, PlanView, deleteCommercial, home, PropietaryView, AddImageCommercialview, AddCommercial, updateCommercial, deleteCommercial,updatePropietary, testUpdate, updatePlanPropietary, AccomodationCommercialList, AccommodationCommercialAdd, deleteAccommodation, test,AccomodationPicturesView
urlpatterns = [
    path('home', home, name='home'),
    path('home/propietary', PropietaryView.as_view(), name='propietary'),
    path('home/propietary/update/<slug:pk>/', updatePropietary, name='updatePropietary'),
    path('home/plan', PlanView.as_view(), name='plan'),
    path('home/plan/update/<slug:pk>/', updatePlanPropietary.as_view(), name='planUpdate'),
    path('home/commercial', CommercialView.as_view(), name='commercial'),
    path('home/commercial/add/', AddCommercial,name='addcommercial'),
    # path('home/commercial/updateCommercial/<slug:pk>/', updateCommercial,name='ACommercial'),
    path('home/commercial/update/<slug:pk>/', updateCommercial,name='updateCommercial'),
    path('home/commercial/delete/<slug:pk>/', deleteCommercial.as_view(),name='deleteCommercial'),
    path('home/commercial/<slug:pk>/Hospedaje', AccomodationCommercialList.as_view(),name='AccomodationCommercialList'),
    path('home/commercial/<slug:pk>/Hospedaje/add', AccommodationCommercialAdd.as_view(),name='AccommodationCommercialAdd'),
    path('home/commercial/<slug:pk>/Hospedaje/update', AccommodationUpdate.as_view(),name='AccommodationUpdate'),
    path('home/commercial/<slug:pk1>/Hospedaje/delete/<slug:id_hospedaje>', deleteAccommodation.as_view(),name='DeleteAccomodation'),
    path('home/commercial/testUpdate/<slug:pk>/', testUpdate.as_view(),name='testUpdate'),
    path('home/test/<slug:pk>', AccomodationPicturesView,name='test'),
    # path('home/test/<slug:pk1>/<slug:pk2>', test,name='test'),
]