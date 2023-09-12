from django.shortcuts import render
from CosatecaApp.models import *

# Create your views here.

def inicio(request):
    productos = Producto.getTodosProductos()
    data= {}
    data['productos'] = productos
    return render(request, 'inicio.html', data)

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def perfil(request, nombreUsuario):
    data= {}
    usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
    productos = Producto.getProductosDeUsuario(usuario)
    data['usuario'] = usuario
    data['productos'] = productos

    return render (request, 'perfil.html', data)

def listadoChats(request):
    data = {}
    nombreUsuario = request.session.get('usuario')
    usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
    listado = Chat.getChatsPorUsuario(usuario.idUsuario)
    data['chats'] = listado
    
    return render (request, 'listadoChats.html', data)