from django.shortcuts import redirect, render
from django.views import View

from CosatecaApp.models import Prestamo, Usuario


class SolicitudesPrestamo(View):
    return_url = None

    def get(self, request):
        data = {}
        nombreUsuario = request.session.get('usuario')
        if nombreUsuario != None:
            usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
            prestamos = Prestamo.getRegistroPrestamosPendientesPorUsuario(usuario.idUsuario)
            data['prestamos'] = prestamos
        
            return render (request, 'solicitudesPrestamo.html', data)
        else:
            return render (request, 'login.html')
        
    def post(self, request):
        postData = request.POST
        respuesta = postData.get('respuesta')
        idPrestamo = postData.get('idPrestamo')

        prestamo = Prestamo.getPrestamoPorId(idPrestamo)
        if respuesta == 'aceptar':
            prestamo.estado = 'Aceptado'
        else:
            prestamo.estado = 'Denegado'
        Prestamo.guardarPrestamo(prestamo)
        return redirect ('/solicitudesPrestamo')