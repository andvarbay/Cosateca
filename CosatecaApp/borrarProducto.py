from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from CosatecaApp.models import Prestamo, Producto, Usuario


class BorrarProducto(View):
    return_url = None

    def get(self, request):
        data = {}
        idProducto = request.GET.get('id')
        producto = Producto.getProductoPorId(idProducto)
        data['producto'] = producto
        return render(request, 'borrarProductoConfirmar.html', data)
    
    def post(self, request):
        postData = request.POST
        respuesta = postData.get('respuesta')
        idProducto = request.GET.get('id')
        producto = Producto.getProductoPorId(idProducto)
        propietario = producto.idPropietario
        current = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario'))
        listaErrores = None
        if respuesta == 'confirmar':
            listaErrores = []
            if current != propietario:
                listaErrores.append('Solo puedes borrar un producto si eres el propietario del mismo. Travieso.')
            if Prestamo.existePrestamoAceptado(propietario,producto):
                listaErrores.append('Este producto está en préstamo actualmente')
            if not listaErrores:
                producto.delete()
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
                data = {
                    'errors': listaErrores,
                    'producto': producto
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