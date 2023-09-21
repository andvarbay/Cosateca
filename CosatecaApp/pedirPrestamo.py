from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Prestamo, Producto, Usuario


class PedirPrestamo(View):
    return_url = None

    def get(self, request):
        data={}
        idPrefijo = request.GET.get('id')
        partes = idPrefijo.split("_")
        idProducto = partes[1]
        producto = Producto.getProductoPorId(idProducto)
        arrendatario = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario'))
        data['producto']=producto
        prestamo = Prestamo.existePrestamoPendiente(arrendatario, producto)
        fecha_inicio_obj = prestamo.fechaInicio
        fecha_inicio_formateada = fecha_inicio_obj.strftime('%d/%m/%Y')
        fecha_fin_obj = prestamo.fechaFin
        fecha_fin_formateada = fecha_fin_obj.strftime('%d/%m/%Y')

        if prestamo:
            values = {
                'fechaInicio': fecha_inicio_formateada,
                'fechaFin': fecha_fin_formateada,
                'condiciones': prestamo.condiciones,
                'longitudCondiciones':len(prestamo.condiciones)
            }
            data['values'] = values
        return render(request, 'pedirPrestamo.html', data)
    def post(self,request):
        postData = request.POST
        idPrefijo = request.GET.get('id')
        partes = idPrefijo.split("_")
        idProducto = partes[1]
        fecha_inicio_str = postData.get('fechaInicio')
        fecha_fin_str = postData.get('fechaFin')
        fecha_inicio_obj = datetime.strptime(fecha_inicio_str, '%d/%m/%Y')  # Convierte la cadena en objeto de fecha
        fecha_fin_obj = datetime.strptime(fecha_fin_str, '%d/%m/%Y')  # Convierte la cadena en objeto de fecha

        fecha_inicio_formateada= datetime.strftime(fecha_inicio_obj, '%d/%m/%Y')
        fecha_fin_formateada= datetime.strftime(fecha_fin_obj, '%d/%m/%Y')

        producto = Producto.getProductoPorId(idProducto)
        arrendador = producto.idPropietario
        arrendatario = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario'))
        condiciones = postData.get('condiciones')
        values = {
                'fechaInicio': fecha_inicio_formateada,
                'fechaFin': fecha_fin_formateada,
                'condiciones': condiciones,
                'longitudCondiciones':len(condiciones)
            }

        listaErrores= []
        if fecha_fin_obj < fecha_inicio_obj:
            listaErrores.append("La fecha de inicio debe ser anterior a la fecha de finalización")
        if fecha_inicio_obj < datetime.now():
            listaErrores.append("La fecha de inicio no puede ser anterior a la fecha actual")
        if listaErrores:
            data = {
                'errors': listaErrores,
                'values': values,
                'producto': producto
            }
            return render(request, 'pedirPrestamo.html', data)
        else:
            prestamo = Prestamo.existePrestamoPendiente(arrendatario,producto)
            prestamo.fechaInicio = fecha_inicio_obj
            prestamo.fechaFin = fecha_fin_obj
            prestamo.condiciones = condiciones
            Prestamo.guardarPrestamo(prestamo)
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

