"""
URL configuration for cosateca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CosatecaApp import views
from CosatecaApp.editarProducto import EditarProducto
from CosatecaApp.login import Login, logout
from CosatecaApp.nuevoProducto import NuevoProducto
from CosatecaApp.register import Register
from CosatecaApp.formularioValoracion import FormularioValoración

from django.conf.urls.static import static
from django.conf import settings

from CosatecaApp.editarPerfil import EditarPerfil

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='catalogo'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout , name='logout'),
    path('perfil/<nombreUsuario>', views.perfil, name='perfil'),
    path('listado-chats/', views.listadoChats, name='listadoChats'),
    path('editarPerfil/<idUsuario>', EditarPerfil.as_view(), name='editarPerfil'),
    path('detallesProducto/<idProducto>',views.detallesProducto, name="detalles"),
    path('realizarValoracion/',FormularioValoración.as_view(), name='realizarValoracion'),
    path('registroPrestamos', views.registroPrestamos, name='registroPrestamos'),
    path('valorarProducto/',FormularioValoración.as_view(), name='valorarProducto'),
    path('nuevoProducto/', NuevoProducto.as_view(), name='nuevoProducto'),
    path('editarProducto/', EditarProducto.as_view(), name='editarProducto'),  
