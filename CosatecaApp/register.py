import hashlib
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from CosatecaApp.models import *
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages

class Register (View):
    def get(self, request):
        return render(request, 'register.html')
  
    def post(self, request):
        postData = request.POST
        nombre = postData.get('nombre')
        apellidos = postData.get('apellidos')
        correo = postData.get('correo')
        ubicacion = postData.get('ubicacion')
        contrasena = postData.get('contrasena')
        contrasena2 = postData.get('contrasena2')
        nombreUsuario = postData.get('nombreUsuario')
        # validation
        values = {
            'nombre': nombre,
            'apellidos': apellidos,
            'ubicacion': ubicacion,
            'correo': correo,
            'nombreUsuario': nombreUsuario
        }
        
        listaErrors = None
  
        usuario = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            contrasena=hashlib.md5(contrasena.encode()).hexdigest(),
            nombreUsuario=nombreUsuario,
            ubicacion=ubicacion,
            rol='usuario')
        listaErrors = self.validarusuario(usuario, contrasena, contrasena2)

        if not listaErrors:                
            return redirect('login')
        else:
            data = {
                'errors': listaErrors,
                'values': values
            }
            return render(request, 'register.html', data)        
  
    def validarusuario(self, usuario, contrasena, contrasena2):
        listaErrores=[]
        if not usuario.nombre:
            listaErrores.append("Introduce tu nombre.")
        if len(usuario.nombre) < 3:
            listaErrores.append("El nombre debe tener al menos 3 caracteres.")
        if not usuario.apellidos:
            listaErrores.append("Introduce tus apellidos.")
        if len(usuario.apellidos) < 3:
            listaErrores.append("Los apellidos deben tener al menos 3 caracteres.")
        if len(contrasena) < 5:
            listaErrores.append("La contraseña debe tener al menos 5 caracteres.")
        if contrasena != contrasena2:
            print(contrasena, contrasena2)
            listaErrores.append("Las contraseñas deben ser iguales.")
        if usuario.correo:
            if len(usuario.correo) < 5:
                listaErrores.append("El correo debe tener más de 5 caracteres.")
            if Usuario.existeCorreo(usuario.correo):
                listaErrores.append("Correo ya registrado.")
        if not usuario.nombreUsuario:
            listaErrores.append("Introduce tu nombre de usuario.")
        if usuario.existe():
            listaErrores.append("Nombre de usuario ya registrado.")
  
        return listaErrores