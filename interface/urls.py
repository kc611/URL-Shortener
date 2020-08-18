from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.base,name="base"),
    path('home/',views.home,name="home"),
    path('account/', views.dashboard),
    path('urlinfo/', views.urlinfo),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"), 
    path('logout/',views.logoutuser,name="logout") ,
    path('<str:id>',views.redirect_views)
]
