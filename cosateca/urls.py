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
from CosatecaApp.borrarPerfil import BorrarPerfil
from CosatecaApp.borrarProducto import BorrarProducto
from CosatecaApp.filtros import Filtros
from CosatecaApp.finalizarPrestamo import FinalizarPrestamo
from CosatecaApp.formularioReporte import FormularioReporte
from CosatecaApp.solicitudesPrestamo import SolicitudesPrestamo
from CosatecaApp.pedirPrestamo import PedirPrestamo
from CosatecaApp.editarProducto import EditarProducto
from CosatecaApp.login import Login, logout
from CosatecaApp.nuevoProducto import NuevoProducto
from CosatecaApp.register import Register
from CosatecaApp.editarPerfil import EditarPerfil
from CosatecaApp.formularioValoracion import FormularioValoración
from CosatecaApp.editarPerfil import EditarPerfil
from django.conf.urls.static import static
from django.conf import settings

from django.urls import include, path

urlpatterns = [
    path("chat/", include("chat.urls")),
    path('admin/', admin.site.urls),
    path('', views.inicio, name='catalogo'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout , name='logout'),
    path('perfil/<nombreUsuario>', views.perfil , name='perfil'),
    path('editarPerfil/', EditarPerfil.as_view() , name='editarPerfil'),
    path('listado-chats/', views.listadoChats, name='listadoChats'),
    path('detallesProducto/<idProducto>',views.detallesProducto, name="detalles"),
    path('valorarProducto/',FormularioValoración.as_view(), name='valorarProducto'),
    path('pedirPrestamo/',PedirPrestamo.as_view(), name = 'pedirPrestamo'),
    path('solicitudesPrestamo/',SolicitudesPrestamo.as_view(), name = 'solicitudesPrestamo'),
    path('finalizarPrestamo/',FinalizarPrestamo.as_view(), name = 'finalizarPrestamo'),
    path('realizarValoracion/',FormularioValoración.as_view(), name='realizarValoracion'),
    path('registroPrestamos', views.registroPrestamos, name='registroPrestamos'),
    path('valorarProducto/',FormularioValoración.as_view(), name='valorarProducto'),
    path('crearChat/<idProducto>', views.crearChat, name='crearChat'),
    path('filtros/',views.filtros, name='filtros'),
    path('nuevoProducto/', NuevoProducto.as_view(), name='nuevoProducto'),
    path('editarProducto/', EditarProducto.as_view(), name='editarProducto'),
    path('logrosEstadisticas/', views.logrosEstadisticas, name='logrosEstadisticasMenu'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('logros/', views.logros, name='logros'),
    path('borrarProducto/', BorrarProducto.as_view(), name='borrarProducto'),
    path('borrarPerfil/', BorrarPerfil.as_view(), name='borrarPerfil'),
    path('realizarReporte/', FormularioReporte.as_view(), name='realizarReporte'),
    path('listados/', views.listados, name='listados'),
    path('productosFavoritos/', views.productosFavoritos, name='productosFavoritos'),
    path('eliminarProductoDeListado/<idListadoProducto>', views.eliminarProductoDeListado, name='eliminarProductoDeListado'),
    path('anadirProductoAFavoritos/<idProducto>', views.anadirProductoAFavoritos, name='anadirProductoAFavoritos'),
    path('usuariosFavoritos/', views.usuariosFavoritos, name='usuariosFavoritos'),
    path('eliminarUsuarioDeListado/<idListadoProducto>', views.eliminarUsuarioDeListado, name='eliminarUsuarioDeListado'),
    path('anadirUsuarioAFavoritos/<idUsuario>', views.anadirUsuarioAFavoritos, name='anadirUsuarioAFavoritos'),
    path('notificaciones', views.notificaciones, name='notificaciones')
    ] 
