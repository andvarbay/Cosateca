from django.shortcuts import redirect, render
from CosatecaApp.models import *
from django.views import View
from CosatecaApp.views import detallesProducto
from datetime import datetime

class EditarProducto(View):
    def get(self, request):
        data = {}
        idProducto = request.GET.get('idProducto')
        producto = Producto.getProductoPorId(idProducto)
        nombreUsuario = request.session.get('usuario')
        if nombreUsuario == producto.idPropietario.nombreUsuario:
            data['categorias'] = Categoria.objects.all()
            categoriasProducto = Producto.getCategoriasDeProducto(producto)
            categorias = [cat.idCategoria.nombre for cat in categoriasProducto]
            values = {
                'idProducto': producto.idProducto,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'categorias': categorias,
            }
            data['values'] = values
            
            return render(request, 'editarProducto.html', data)
        else:
            return render(request, 'detalles',idProducto = producto.idProducto)
    
    def post(self, request):
        postData = request.POST
        nombre = postData.get('nombre')
        descripcion = postData.get('descripcion')
        categorias = request.POST.getlist('categorias')
        fotoProducto = request.FILES.get('fotoProducto')
        idProducto = postData.get('idProducto')
        print('CATEGORIAS::::::', categorias)

        if fotoProducto:
            foto = PrivateAttachment(
                file = fotoProducto
            )
            PrivateAttachment.nuevaFoto(foto)
            producto.fotoProducto = foto
        producto = Producto.getProductoPorId(idProducto)
        producto.nombre = nombre
        producto.descripcion = descripcion
        Producto.guardarProducto(producto)

        todasCategorias = Categoria.objects.all()
        for cat in todasCategorias:
            existe = CategoriaProducto.existeCategoriaProducto(cat, producto)            
            if cat.nombre in categorias:
                if existe == False:
                    catprod = CategoriaProducto(
                        idCategoria = cat,
                        idProducto = producto
                    )
                    CategoriaProducto.nuevaCategoriaProducto(catprod)
            else:
                if existe:
                    CategoriaProducto.delete(existe)

        return redirect('detalles', idProducto = producto.idProducto)