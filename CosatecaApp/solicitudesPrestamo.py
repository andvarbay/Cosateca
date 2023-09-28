from datetime import datetime
from django.shortcuts import redirect, render
from django.views import View

from CosatecaApp.models import Estadistica, EstadisticaUsuario, Logro, LogroUsuario, Prestamo, Usuario


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
            return render (request, 'solicitudesPrestamo.html', data)

        Prestamo.guardarPrestamo(prestamo)
        participado = Estadistica.getEstadisticaPorNombre('Préstamos realizados')
        arrendador = Estadistica.getEstadisticaPorNombre('Préstamos como arrendador')
        arrendatario = Estadistica.getEstadisticaPorNombre('Préstamos como arrendatario')
        
        #Logro participar en un préstamo aceptado
        estusu = EstadisticaUsuario.getEstadisticaUsuario(participado, prestamo.idArrendador)
        estusu.valor += 1
        estusu.save()
        self.LogroParticiparEnPrestamos(estusu.valor, prestamo.idArrendador)

        estusu = EstadisticaUsuario.getEstadisticaUsuario(participado, prestamo.idArrendatario)
        estusu.valor += 1
        estusu.save()
        self.LogroParticiparEnPrestamos(estusu.valor, prestamo.idArrendatario)

        #Logro participar como arrendador
        estusu = EstadisticaUsuario.getEstadisticaUsuario(arrendador, prestamo.idArrendador)
        estusu.valor += 1
        estusu.save()
        self.LogroParticiparComoArrendador(estusu.valor, prestamo.idArrendador)

        #Logro participar como arrendatario
        estusu = EstadisticaUsuario.getEstadisticaUsuario(arrendatario, prestamo.idArrendatario)
        estusu.valor += 1
        estusu.save()
        self.LogroParticiparComoArrendatario(estusu.valor, prestamo.idArrendatario)



        return redirect ('/solicitudesPrestamo')
    def LogroParticiparEnPrestamos(self, valor, usuario):
        if valor == 1:
            logro = Logro.GetLogroPorNombre('Negocio local')
            self.obtenerLogro(logro, usuario)
        elif valor == 5:
            logro = Logro.GetLogroPorNombre('Hombre de negocios')
            self.obtenerLogro(logro, usuario)
        elif valor == 10:
            logro = Logro.GetLogroPorNombre('Usuario de honor')
            self.obtenerLogro(logro, usuario)

    def LogroParticiparComoArrendador(self, valor, usuario):
        if valor == 1:
            logro = Logro.GetLogroPorNombre('Arrendador primerizo')
            self.obtenerLogro(logro, usuario)
        elif valor == 5:
            logro = Logro.GetLogroPorNombre('Arrendador ocasional')
            self.obtenerLogro(logro, usuario)
        elif valor == 10:
            logro = Logro.GetLogroPorNombre('Arrendando que es gerundio')
            self.obtenerLogro(logro, usuario)

    def LogroParticiparComoArrendatario(self, valor, usuario):
        if valor == 1:
            logro = Logro.GetLogroPorNombre('Arrendatario primerizo')
            self.obtenerLogro(logro, usuario)
        elif valor == 5:
            logro = Logro.GetLogroPorNombre('Arrendatario ocasional')
            self.obtenerLogro(logro, usuario)
        elif valor == 10:
            logro = Logro.GetLogroPorNombre('Arrendatando que es gerundio')
            self.obtenerLogro(logro, usuario)

    def obtenerLogro(self, logro, usuario):
        logrosu = LogroUsuario(
            idLogro=logro,
            idUsuario=usuario,
            fechaObtencion=datetime.now()
        )
        logrosu.save()
