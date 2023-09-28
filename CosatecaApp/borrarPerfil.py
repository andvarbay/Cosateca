from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from CosatecaApp.models import Prestamo, Producto, Usuario


class BorrarPerfil(View):
    return_url = None

    def get(self, request):
        return render(request, 'borrarPerfilConfirmar.html')
    
    def post(self, request):
        postData = request.POST
        respuesta = postData.get('respuesta')
        current = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario'))
        if respuesta == 'confirmar':
            current.delete()
            request.session.clear()
            response_html = f"""
            <html>
            <head>
                <script>
                if (window.opener && !window.opener.closed) {{
                    window.opener.location.href = '{reverse('catalogo')}';  // Redirige a la ruta '/'
                    window.opener.focus();
                }}
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