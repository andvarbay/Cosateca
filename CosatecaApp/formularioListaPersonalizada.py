from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Estadistica, EstadisticaUsuario, Listado, Logro, LogroUsuario, Producto, Reporte, Usuario, Valoracion


class FormularioListaPersonalizada(View):
    return_url = None

    def get(self, request):
        data = {}
        nombreUsuario = request.session.get('usuario')
        if nombreUsuario == None:
            response_html = """
            <html>
            <head>
                <script>
                if (window.opener && !window.opener.closed) {
                    window.opener.location.href = '/login'; // Redirige la ventana anterior a /login
                    window.opener.focus(); // Enfoca la ventana anterior
                }
                window.close(); // Cierra la ventana actual
                </script>
            </head>
            <body>
                <p>Formulario procesado con éxito. Esta ventana se cerrará automáticamente.</p>
            </body>
            </html>
            """
            return HttpResponse(response_html)

        return render(request, 'formularioListaPersonalizada.html', data)

            
    def post(self, request):
        postData = request.POST
        nombre = postData.get('nombre')
        userNameEmisor = request.session.get('usuario')
        propietario = Usuario.getUsuarioPorNombreUsuario(userNameEmisor)

        listado = Listado(
            nombre=nombre,
            idPropietario=propietario
        )
        listado.save()

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
    
    