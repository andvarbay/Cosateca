import hashlib
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from minio import Minio
from CosatecaApp.models import PrivateAttachment, Usuario
from cosateca.settings import SECRETS

client = Minio(
                SECRETS['MINIO_ENDPOINT'],
                access_key = SECRETS['MINIO_ACCESS_KEY'],
                secret_key = SECRETS['MINIO_SECRET_KEY']
            )

class EditarPerfil (View):
    def get(self, request, idUsuario):
        data = {}
        current = Usuario.getUsuarioPorId(idUsuario)
        values = {
            'nombre': current.nombre,
            'apellidos': current.apellidos,
            'ubicacion': current.ubicacion,
            'correo': current.correo,
            'nombreUsuario': current.nombreUsuario,
        }
        data['values'] = values
        return render(request, 'editarPerfil.html', data)
    
    def post(self,request, idUsuario):
        postData = request.POST
        nombre = postData.get('nombre')
        apellidos = postData.get('apellidos')
        correo = postData.get('correo')
        ubicacion = postData.get('ubicacion')
        contrasena = postData.get('contrasena')
        contrasenaNueva = postData.get('contrasenaNueva')
        contrasenaNueva2 = postData.get('contrasenaNueva2')
        nombreUsuario = postData.get('nombreUsuario')
        fotoPerfil = request.FILES.get('fotoPerfil')
        # validation
        values = {
            'nombre': nombre,
            'apellidos': apellidos,
            'ubicacion': ubicacion,
            'correo': correo,
            'nombreUsuario': nombreUsuario,
        }
        foto = PrivateAttachment(
            file = fotoPerfil
        )
        PrivateAttachment.nuevaFoto(foto)
        
        listaErrores = None
        current = Usuario.getUsuarioPorNombreUsuario(idUsuario)
        listaErrores = self.validarUsuario(idUsuario, nombre, apellidos, correo, nombreUsuario, contrasena, contrasenaNueva, contrasenaNueva2)
        if not listaErrores:
            current.nombre = nombre
            current.apellidos = apellidos
            current.correo = correo
            current.ubicacion = ubicacion
            current.contrasena = contrasenaNueva
            current.nombreUsuario = nombreUsuario
            if fotoPerfil != None:
                # print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ      ' + str(current.fotoPerfil.file))
                # client.remove_object("django-backend-dev-public", str(current.fotoPerfil.file))
                current.fotoPerfil= foto
            current.contrasena = hashlib.md5(contrasenaNueva.encode()).hexdigest()
            Usuario.registro(current)
            request.session['usuario'] = current.nombreUsuario
            request.session['usuarioFoto'] = str(current.fotoPerfil.file)
            return redirect('perfil', current.nombreUsuario)
        else:
            data = {
                'errors' : listaErrores,
                'values' : values
            }
            return render(request, 'editarPerfil.html',data)
    def validarUsuario(self, idUsuario, nombre, apellidos, correo, nombreUsuario, contrasenaActual, contrasenaNueva , contrasenaNueva2):
        listaErrores=[]
        current = Usuario.getUsuarioPorNombreUsuario(idUsuario)
        if len(nombre) < 3:
            listaErrores.append("El nombre debe tener al menos 3 caracteres.")
        if len(apellidos) < 3:
            listaErrores.append("Los apellidos deben tener al menos 3 caracteres.")
        if ((contrasenaActual != '') | (contrasenaNueva!= '') | (contrasenaNueva2!='')):
            contrasena_md5 = hashlib.md5(contrasenaActual.encode()).hexdigest()
            if contrasena_md5 != current.contrasena:
                listaErrores.append("Contraseña actual incorrecta")
            if len(contrasenaNueva) < 5:
                listaErrores.append("La contraseña debe tener al menos 5 caracteres.")
            if contrasenaNueva != contrasenaNueva2:
                listaErrores.append("Las contraseñas deben ser iguales.")
        if correo:
            if len(correo) < 5:
                listaErrores.append("El correo debe tener más de 5 caracteres.")
            if ((correo != current.correo) & Usuario.existeCorreo(correo)):
                listaErrores.append("Correo ya registrado.")
        if ((nombreUsuario != current.nombreUsuario) & (Usuario.getUsuarioPorNombreUsuario(nombreUsuario) != False)):
            listaErrores.append("Nombre de usuario ya registrado.")

        return listaErrores