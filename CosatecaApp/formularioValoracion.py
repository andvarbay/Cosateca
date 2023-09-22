from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Estadistica, EstadisticaUsuario, Logro, LogroUsuario, Producto, Usuario, Valoracion


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
                receptor = Usuario.getUsuarioPorId(producto.idProducto)
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
                if estusu.valor == 1:
                    logro = Logro.GetLogroPorNombre('Libertad de expresión')
                    logrousu= LogroUsuario(
                    idLogro= logro,
                    idUsuario=emisor,
                    fechaObtencion=datetime.now()
                    )
                    logrousu.save()
                elif estusu.valor == 5:
                    logro = Logro.GetLogroPorNombre('Valorando el mercado')
                    logrousu= LogroUsuario(
                    idLogro= logro,
                    idUsuario=emisor,
                    fechaObtencion=datetime.now()
                    )
                    logrousu.save()
                elif estusu.valor == 10:
                    logro = Logro.GetLogroPorNombre('El juez')
                    logrousu= LogroUsuario(
                    idLogro= logro,
                    idUsuario=emisor,
                    fechaObtencion=datetime.now()
                    )
                    logrousu.save()
                estadistica = Estadistica.getEstadisticaPorNombre('Valoraciones recibidas')
                estusu = EstadisticaUsuario.getEstadisticaUsuario(estadistica, receptor)
                estusu.valor += 1
                estusu.save()
                if estusu.valor == 1:
                    logro = Logro.GetLogroPorNombre('En el punto de mira')
                    logrousu= LogroUsuario(
                    idLogro= logro,
                    idUsuario=receptor,
                    fechaObtencion=datetime.now()
                    )
                    logrousu.save()
                elif estusu.valor == 5:
                    logro = Logro.GetLogroPorNombre('La vieja confiable')
                    logrousu= LogroUsuario(
                    idLogro= logro,
                    idUsuario=receptor,
                    fechaObtencion=datetime.now()
                    )
                    logrousu.save()
                elif estusu.valor == 10:
                    logro = Logro.GetLogroPorNombre('Solo Dios puede juzgarme')
                    logrousu= LogroUsuario(
                    idLogro= logro,
                    idUsuario=receptor,
                    fechaObtencion=datetime.now()
                    )
                    logrousu.save()

            else:
                valoracion.puntuacion = puntuacion
                valoracion.comentario = comentario
                Valoracion.guardarValoracion(valoracion)                
                
            


        else:
            partes = idPrefijo.split("_")
            idUsuario = partes[1]
            receptor = Usuario.getUsuarioPorId(idUsuario)
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
            if estusu.valor == 1:
                logro = Logro.GetLogroPorNombre('Libertad de expresión')
                logrousu= LogroUsuario(
                idLogro= logro,
                idUsuario=emisor,
                fechaObtencion=datetime.now()
                )
                logrousu.save()
            elif estusu.valor == 5:
                logro = Logro.GetLogroPorNombre('Valorando el mercado')
                logrousu= LogroUsuario(
                idLogro= logro,
                idUsuario=emisor,
                fechaObtencion=datetime.now()
                )
                logrousu.save()
            elif estusu.valor == 10:
                logro = Logro.GetLogroPorNombre('El juez')
                logrousu= LogroUsuario(
                idLogro= logro,
                idUsuario=emisor,
                fechaObtencion=datetime.now()
                )
                logrousu.save()
                


            estadistica = Estadistica.getEstadisticaPorNombre('Valoraciones recibidas')
            estusu = EstadisticaUsuario.getEstadisticaUsuario(estadistica, receptor)
            estusu.valor += 1
            estusu.save()
            if estusu.valor == 1:
                logro = Logro.GetLogroPorNombre('En el punto de mira')
                logrousu= LogroUsuario(
                idLogro= logro,
                idUsuario=receptor,
                fechaObtencion=datetime.now()
                )
                logrousu.save()
            elif estusu.valor == 5:
                logro = Logro.GetLogroPorNombre('La vieja confiable')
                logrousu= LogroUsuario(
                idLogro= logro,
                idUsuario=receptor,
                fechaObtencion=datetime.now()
                )
                logrousu.save()
            elif estusu.valor == 10:
                logro = Logro.GetLogroPorNombre('Solo Dios puede juzgarme')
                logrousu= LogroUsuario(
                idLogro= logro,
                idUsuario=receptor,
                fechaObtencion=datetime.now()
                )
                logrousu.save()

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