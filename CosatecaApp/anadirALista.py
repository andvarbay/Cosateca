from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Listado, ListadoProducto, Producto, Usuario


class AnadirALista(View):

    def get(self, request, idProducto):
        data = {}
        nombreUsuario = request.session.get('usuario')
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
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
        producto = Producto.getProductoPorId(idProducto)
        listas = Listado.getListasPersonalidazas(usuario.idUsuario)
        data['listas'] = listas
        data['producto'] = producto
        return render(request, 'anadirALista.html', data)

    def post(self, request, idProducto):
        postData = request.POST
        idListado = postData.get('listaPersonalizada')
        producto = Producto.getProductoPorId(idProducto)
        nombreUsuario = request.session.get('usuario')
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)

        if idListado != "":
            listado = Listado.getListadoPorId(idListado)             
            existenIguales = ListadoProducto.existenListadosIguales(listado,producto,usuario)
            print(listado, producto, usuario)
            if not existenIguales:
                lp = ListadoProducto(
                    idListado = listado,
                    idProducto = producto,
                    idUsuario = usuario,
                    fechaAdicion = datetime.now()
                )
                lp.save()
                
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
