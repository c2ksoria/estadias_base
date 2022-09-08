from django.contrib import admin
from django.urls import path, include
from .views import  CommercialView, PlanView, deleteCommercial, home, PropietaryView, AddImageCommercialview, AddCommercial, updateCommercial, deleteCommercial,updatePropietary, testUpdate, updatePlanPropietary
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
    path('home/commercial/testUpdate/<slug:pk>/', testUpdate.as_view(),name='testUpdate'),
]

