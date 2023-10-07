from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Estadistica, EstadisticaUsuario, Logro, LogroUsuario, Producto, Reporte, Usuario, Valoracion


class FormularioReporte(View):
    return_url = None

    def get(self, request):
        data = {}
        idPrefijo = request.GET.get('id')
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
        if idPrefijo.startswith('p_'):
            partes = idPrefijo.split("_")
            idProducto = partes[1]
            producto = Producto.getProductoPorId(idProducto)
            data['producto'] = producto
            idEmisor = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario')).idUsuario
            if Reporte.getReporteProducto(idEmisor, idProducto):
                reporte = Reporte.getReporteProducto(idEmisor, idProducto)
                values = {
                    'descripcion': reporte.descripcion,
                    'longitudComentario':len(reporte.descripcion)
                }
                data['values'] = values
            
        else:
            partes = idPrefijo.split("_")
            idUsuario = partes[1]
            usuario = Usuario.getUsuarioPorId(idUsuario)
            data['usuario'] = usuario
            idEmisor = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario')).idUsuario
            if Reporte.getReporteProducto(idEmisor,usuario.idUsuario):
                reporte = Reporte.getReporteProducto(idEmisor,usuario.idUsuario)
                values = {
                    'puntuacion':reporte.puntuacion,
                    'comentario': reporte.comentario,
                }
                data['values'] = values

        return render(request, 'formularioReporte.html', data)
    
    def post(self, request):
        postData = request.POST
        descripcion = postData.get('descripcion')
        userNameEmisor = request.session.get('usuario')
        emisor = Usuario.getUsuarioPorNombreUsuario(userNameEmisor)
        idPrefijo = request.GET.get('id')
        if idPrefijo.startswith('p_'):
            partes = idPrefijo.split("_")
            idProducto = partes[1] 
            reporte = Reporte.getReporteProducto(emisor.idUsuario,idProducto)   
            if reporte == False:
                producto = Producto.getProductoPorId(idProducto)
                receptor = producto.idPropietario
                reporte = Reporte(    
                    idEmisor = emisor,
                    idReceptor = receptor,
                    descripcion = descripcion,
                    idProducto = producto,
                    fechaHora = datetime.now()
                )
                reporte.save()

            else:
                reporte.descripcion = descripcion
                reporte.fechaHora = datetime.now()
                reporte.save()
                
            


        else:
            partes = idPrefijo.split("_")
            idUsuario = partes[1]
            receptor = Usuario.getUsuarioPorId(idUsuario)
            reporte = Reporte.getReporteUsuario(emisor.idUsuario,receptor.idUsuario)
            if reporte == False:
                reporte = Reporte(
                    idEmisor = emisor,
                    idReceptor = receptor,
                    descripcion = descripcion,
                    fechaHora = datetime.now(),
                )
            else:
                reporte.descripcion = descripcion
                reporte.fechaHora = datetime.now()
            reporte.save()


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
    
    