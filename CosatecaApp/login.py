from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from CosatecaApp.models import *
from django.views import View
import hashlib


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        nombreUsuario = request.POST.get ('nombreUsuario')
        contrasena = request.POST.get ('contrasena')
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        mensajeError = None
        if usuario:
            contrasena_md5 = hashlib.md5(contrasena.encode()).hexdigest()
            if contrasena_md5 == usuario.contrasena:
                request.session['usuario'] = usuario.nombreUsuario
                request.session['usuarioFoto'] = str(usuario.fotoPerfil.file)
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('catalogo')
            else:
                mensajeError = 'Contraseña incorrecta'
        else:
            mensajeError = 'Nombre de usuario no existe'
            
        return render (request, 'login.html', {'error': mensajeError})

def logout(request):
    request.session.clear()
    return redirect('catalogo')

