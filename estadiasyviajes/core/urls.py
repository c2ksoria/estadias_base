from django.contrib import admin
from django.urls import path, include
from .views import CommercialView, PlanView, home, PropietaryView
urlpatterns = [
    path('home', home, name='home'),
    path('home/propietary', PropietaryView.as_view(), name='propietary'),
    path('home/plan', PlanView.as_view(), name='plan'),
    path('home/commercial', CommercialView.as_view(), name='commercial'),
]