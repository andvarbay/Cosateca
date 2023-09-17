from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Producto, Usuario, Valoracion


class FormularioValoración(View):
    return_url = None

    def get(self, request):
        data = {}
        idPrefijo = request.GET.get('id')
        if idPrefijo.startswith('p_'):
            partes = idPrefijo.split("_")
            idProducto = partes[1]
            producto = Producto.getProductoPorId(idProducto)
            data['valorado'] = 'producto'
            data['producto'] = producto
            idEmisor = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario')).idUsuario
            if Valoracion.existeValoracionProducto(idEmisor, producto.idProducto):
                valoracion = Valoracion.getValoracionProducto(idEmisor, producto.idProducto)
                values = {
                    'puntuacion':valoracion.puntuacion,
                    'comentario': valoracion.comentario,
                }
                data['values'] = values
            
        else:
            partes = idPrefijo.split("_")
            idUsuario = partes[1]
            usuario = Usuario.getUsuarioPorId(idUsuario)
            data['valorado'] = 'usuario'
            data['usuario'] = usuario
        return render(request, 'formularioValoracion.html', data)
    
    def post(self, request):
        postData = request.POST
        puntuacion = postData.get('puntuacion')
        comentario = postData.get('comentario')
        userNameEmisor = postData.get('idEmisor')
        emisor = Usuario.getUsuarioPorNombreUsuario(userNameEmisor)
        idPrefijo = request.GET.get('id')
        if idPrefijo.startswith('p_'):
            partes = idPrefijo.split("_")
            idProducto = partes[1] 
            valoracion = Valoracion.getValoracionProducto(emisor.idUsuario,idProducto)   
            if valoracion == False:
                producto = Producto.getProductoPorId(idProducto)
                receptor = Usuario.getUsuarioPorId(producto.idProducto)
                valoracion = Valoracion(
                    idEmisor = emisor,
                    idReceptor = receptor,
                    puntuacion = puntuacion,
                    comentario = comentario,
                    idProducto = producto
                )
            else:
                valoracion.puntuacion = puntuacion
                valoracion.comentario = comentario
            valoracion.guardarValoracion()
            


        else:
            partes = idPrefijo.split("_")
            idUsuario = partes[1]
            usuario = Usuario.getUsuarioPorId(idUsuario)
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