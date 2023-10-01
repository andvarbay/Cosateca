from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Prestamo, Usuario, Notificacion


class FinalizarPrestamo(View):
    return_url = None

    def get(self, request):
        data = {}
        idPrefijo = request.GET.get('id')
        partes = idPrefijo.split("_")
        idPrestamo = partes[1]
        prestamo = Prestamo.getPrestamoPorId(idPrestamo)
        data['prestamo'] = prestamo
        return render(request, 'finalizarPrestamoConfirmar.html', data)
    
    def post(self, request):
        postData = request.POST
        respuesta = postData.get('respuesta')
        idPrefijo = request.GET.get('id')
        partes = idPrefijo.split("_")
        idPrestamo = partes[1]
        prestamo = Prestamo.getPrestamoPorId(idPrestamo)
        arrendador = prestamo.idArrendador
        current = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario'))
        listaErrores = None
        if respuesta == 'confirmar':
            listaErrores = []
            if current != arrendador:
                listaErrores.append('Solo puedes finalizar un préstamo si eres el arrendador del mismo. Travieso.')
            if prestamo.estado != 'Aceptado':
                listaErrores.append('Solo puedes finalizar préstamos activos')
            if not listaErrores:
                prestamo.estado = 'Finalizado'
                prestamo.idProducto.disponibilidad = 1
                prestamo.idProducto.save()
                Prestamo.guardarPrestamo(prestamo)
                Notificacion.guardarNotificacion(idUsuario = prestamo.idArrendador, tipo="finPrestamo", concatenacion=str(prestamo.idProducto.nombre))
                Notificacion.guardarNotificacion(idUsuario = prestamo.idArrendatario, tipo="finPrestamo", concatenacion=str(prestamo.idProducto.nombre))
                response_html = """
                <html>
                <head>
                    <script>
                    if (window.opener && !window.opener.closed) {
                        window.opener.location.reload();
                    }
                    window.close();
                </script>
                </head>
                <body>
                    <p>Formulario procesado con éxito. Esta ventana se cerrará automáticamente.</p>
                </body>
                </html>
                """
                return HttpResponse(response_html)
            else:
                data = {
                    'errors': listaErrores,
                    'prestamo': prestamo
                }
                return render(request, 'finalizarPrestamoConfirmar.html', data)
            
        else:
            response_html = """
                <html>
                <head>
                    <script>
                    if (window.opener && !window.opener.closed) {
                        window.opener.location.reload();
                    }
                    window.close();
                </script>
                </head>
                <body>
                    <p>Formulario procesado con éxito. Esta ventana se cerrará automáticamente.</p>
                </body>
                </html>
                """
            return HttpResponse(response_html)