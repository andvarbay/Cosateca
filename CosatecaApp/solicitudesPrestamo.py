from django.shortcuts import redirect, render
from django.views import View

from CosatecaApp.models import Estadistica, EstadisticaUsuario, Prestamo, Usuario


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
            p = Prestamo.existePrestamoAceptado(prestamo.idArrendador,prestamo.idProducto)
            if p:
                prestamos = Prestamo.getRegistroPrestamosPendientesPorUsuario(prestamo.idArrendador)            
                data = {
                    'prestamos': prestamos,
                    'error': f'No puedes aceptar la solicitud de {p.idProducto.nombre} porque ya se lo estás prestando a {p.idArrendatario.nombreUsuario} ahora mismo.'
                }
                return render (request, 'solicitudesPrestamo.html', data)
            else:
                prestamo.estado = 'Aceptado'
                prestamo.idProducto.disponibilidad = 0
                prestamo.idProducto.save()
        else:
            prestamo.estado = 'Denegado'
        Prestamo.guardarPrestamo(prestamo)
        participado = Estadistica.getEstadisticaPorNombre('Préstamos realizados')
        arrendador = Estadistica.getEstadisticaPorNombre('Préstamos como arrendador')
        arrendatario = Estadistica.getEstadisticaPorNombre('Préstamos como arrendatario')
        
        #Logro participar en un préstamo aceptado
        estusu = EstadisticaUsuario.getEstadisticaUsuario(participado, prestamo.idArrendador)
        estusu.valor += 1
        estusu.save()
        estusu = EstadisticaUsuario.getEstadisticaUsuario(participado, prestamo.idArrendatario)
        estusu.valor += 1
        estusu.save()

        #Logro participar como arrendador
        estusu = EstadisticaUsuario.getEstadisticaUsuario(arrendador, prestamo.idArrendador)
        estusu.valor += 1
        estusu.save()

        #Logro participar como arrendatario
        estusu = EstadisticaUsuario.getEstadisticaUsuario(arrendatario, prestamo.idArrendatario)
        estusu.valor += 1
        estusu.save()



        return redirect ('/solicitudesPrestamo')