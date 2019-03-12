from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('product/', views.product, name='shopoholic-product'),
    path('sort/', views.sort_home, name='shopoholic-sort'),
    path('register/', views.register, name='shopoholic-register'),

]