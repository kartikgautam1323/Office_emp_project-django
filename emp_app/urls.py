from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('all_emp', views.all_emp,name='all_emp'),
    path('add_emp', views.add_emp,name='add_emp'),
    path('remove_emp', views.remove_emp,name='remove_emp'),
    path('filter_emp', views.filter_emp,name='filter_emp'),
    path('signup/', views.handlesignup,name='handlesignup'),
    path('login/', views.handlelogin,name='handlelogin'),
    path('logout/', views.handlelogout,name='handlelogout'),
    
]