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
        
        for cat in categorias:
            c = Categoria.getCategoriaPorNombre(cat)
            catprod = CategoriaProducto(
                idCategoria = c,
                idProducto = producto
            )
            CategoriaProducto.nuevaCategoriaProducto(catprod)

        return redirect('detalles', idProducto = producto.idProducto)