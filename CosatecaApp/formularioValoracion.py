from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Estadistica, EstadisticaUsuario, Logro, LogroUsuario, Notificacion, Producto, Usuario, Valoracion


class FormularioValoración(View):
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
            data['valorado'] = 'producto'
            data['producto'] = producto
            idEmisor = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario')).idUsuario
            if idEmisor == producto.idPropietario:
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
            if Valoracion.existeValoracionProducto(idEmisor, producto.idProducto):
                valoracion = Valoracion.getValoracionProducto(idEmisor, producto.idProducto)
                values = {
                    'puntuacion':valoracion.puntuacion,
                    'comentario': valoracion.comentario,
                    'longitudComentario':len(valoracion.comentario)
                    
                }
                data['values'] = values
            
        else:
            partes = idPrefijo.split("_")
            idUsuario = partes[1]
            usuario = Usuario.getUsuarioPorId(idUsuario)
            data['valorado'] = 'usuario'
            data['usuario'] = usuario
            idEmisor = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario')).idUsuario
            if Valoracion.existeValoracionUsuario(idEmisor,usuario.idUsuario):
                valoracion = Valoracion.getValoracionUsuario(idEmisor, usuario.idUsuario)
                values = {
                    'puntuacion':valoracion.puntuacion,
                    'comentario': valoracion.comentario,
                }
                data['values'] = values

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
                receptor = Usuario.getUsuarioPorId(producto.idPropietario.idUsuario)
                valoracion = Valoracion(    
                    idEmisor = emisor,
                    idReceptor = receptor,
                    puntuacion = puntuacion,
                    comentario = comentario,
                    idProducto = producto
                )
                valoracion.guardarValoracion()

                estadistica = Estadistica.getEstadisticaPorNombre('Comentarios publicados')
                estusu = EstadisticaUsuario.getEstadisticaUsuario(estadistica, emisor)
                estusu.valor += 1
                estusu.save()
                self.LogroPublicarValoracion(estusu.valor, emisor)

                estadistica = Estadistica.getEstadisticaPorNombre('Valoraciones recibidas')
                estusu = EstadisticaUsuario.getEstadisticaUsuario(estadistica, receptor)
                estusu.valor += 1
                estusu.save()
                self.LogroRecibirValoracion(estusu.valor, receptor)
            else:
                valoracion.puntuacion = puntuacion
                valoracion.comentario = comentario
                Valoracion.guardarValoracion(valoracion)                
                
            


        else:
            partes = idPrefijo.split("_")
            idUsuario = partes[1]
            receptor = Usuario.getUsuarioPorId(idUsuario)
            if emisor == receptor:
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

            valoracion = Valoracion.getValoracionUsuario(emisor.idUsuario,receptor.idUsuario)
            if valoracion == False:
                valoracion = Valoracion(
                    idEmisor = emisor,
                    idReceptor = receptor,
                    puntuacion = puntuacion,
                    comentario = comentario,
                )
            else:
                valoracion.puntuacion = puntuacion
                valoracion.comentario = comentario
            valoracion.guardarValoracion()
            estadistica = Estadistica.getEstadisticaPorNombre('Comentarios publicados')
            estusu = EstadisticaUsuario.getEstadisticaUsuario(estadistica, emisor)
            estusu.valor += 1
            estusu.save()
            self.LogroPublicarValoracion(estusu.valor, emisor)

                


            estadistica = Estadistica.getEstadisticaPorNombre('Valoraciones recibidas')
            estusu = EstadisticaUsuario.getEstadisticaUsuario(estadistica, receptor)
            estusu.valor += 1
            estusu.save()
            self.LogroRecibirValoracion(estusu.valor, receptor)


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
    
    def obtenerLogro(self, logro, usuario):
        logrosu = LogroUsuario(
            idLogro=logro,
            idUsuario=usuario,
            fechaObtencion=datetime.now()
        )
        logrosu.save()
        Notificacion.guardarNotificacion(idUsuario=usuario, tipo="desbloqueoLogro", concatenacion=str(logrosu.idLogro.nombre))

    def LogroPublicarValoracion(self, valor, usuario):
        if valor == 1:
            logro = Logro.GetLogroPorNombre('Libertad de expresión')
            self.obtenerLogro(logro, usuario)
        elif valor == 5:
            logro = Logro.GetLogroPorNombre('Valorando el mercado')
            self.obtenerLogro(logro, usuario)
        elif valor == 10:
            logro = Logro.GetLogroPorNombre('El juez')
            self.obtenerLogro(logro, usuario)

    def LogroRecibirValoracion(self, valor, usuario):
        if valor == 1:
            logro = Logro.GetLogroPorNombre('En el punto de mira')
            self.obtenerLogro(logro, usuario)
        elif valor == 5:
            logro = Logro.GetLogroPorNombre('La vieja confiable')
            self.obtenerLogro(logro, usuario)
        elif valor == 10:
            logro = Logro.GetLogroPorNombre('Solo Dios puede juzgarme')
            self.obtenerLogro(logro, usuario)

