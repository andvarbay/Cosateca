from django.shortcuts import redirect, render
from CosatecaApp.models import *
from django.views import View
from CosatecaApp.views import detallesProducto
from datetime import datetime

class NuevoProducto(View):
    def get(self, request):
        data = {}
        nombreUsuario = request.session.get('usuario')
        if nombreUsuario != None:
            usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
            categorias = Categoria.objects.all()
            data['categorias'] = categorias
            
            return render(request, 'nuevoProducto.html', data)
        else:
            return render(request, 'login.html')
    
    def post(self, request):
        postData = request.POST
        nombre = postData.get('nombre')
        descripcion = postData.get('descripcion')
        categorias = request.POST.getlist('categorias')
        fotoProducto = request.FILES.get('fotoProducto')
        propietario = Usuario.getUsuarioPorNombreUsuario(request.session.get('usuario'))

        if not fotoProducto:
            foto = None
        else:
            foto = PrivateAttachment(
                file = fotoProducto
            )
            PrivateAttachment.nuevaFoto(foto)

        producto = Producto(
            nombre = nombre,
            descripcion = descripcion,
            disponibilidad = True,
            idPropietario = propietario,
            fechaSubida = datetime.now(),
            fotoProducto = foto
        )
        Producto.guardarProducto(producto)

        #ESTADISTICAS Y LOGROS =============================
        estadistica = Estadistica.getEstadisticaPorNombre('Productos subidos')
        estusu = EstadisticaUsuario.getEstadisticaUsuario(estadistica, propietario)
        estusu.valor += 1
        estusu.save()
        if estusu.valor==1:
            logro = Logro.GetLogroPorNombre('Proveedor novato')
            print(logro,'ASDASDSADASDASDASDASDDAASD',propietario)
            self.obtenerLogro(logro, propietario)
        elif estusu.valor==5:
            logro = Logro.GetLogroPorNombre('Proveedor intermedio')
            self.obtenerLogro(logro, propietario)
        elif estusu.valor==10:
            logro = Logro.GetLogroPorNombre('Proveedor experto')
            self.obtenerLogro(logro, propietario)

        #ESTADISTICAS Y LOGROS =============================
        
        
        for cat in categorias:
            c = Categoria.getCategoriaPorNombre(cat)
            catprod = CategoriaProducto(
                idCategoria = c,
                idProducto = producto
            )
            CategoriaProducto.nuevaCategoriaProducto(catprod)

        return redirect('detalles', idProducto = producto.idProducto)
    
    def obtenerLogro(self, logro, usuario):
        logrosu = LogroUsuario(
            idLogro=logro,
            idUsuario=usuario,
            fechaObtencion=datetime.now()
        )
        logrosu.save()