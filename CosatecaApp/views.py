import datetime
from django.shortcuts import redirect, render
from CosatecaApp.models import *

# Create your views here.

def inicio(request):
    data= {}
    busqueda = request.GET.get('buscar', None)
    orden = request.GET.get('orden')
    disponible = request.GET.get('disponible')
    categorias_str = request.GET.get('categorias')


    if busqueda == None:
        productos = Producto.objects.all()
    else:
        productos = Producto.getProductosPorTexto(busqueda)
    if orden == 'nuevos':
        productos = productos.order_by('-fechaSubida')
    if disponible == 'disponible':
        productos = productos.filter(disponibilidad=True)
    if categorias_str:
        categorias = categorias_str.split('*')
        for cat in categorias:
            productos = productos.filter(categoriaproducto__idCategoria__nombre=cat)
            productos = productos.distinct()


    data['productos'] = productos
    return render(request, 'inicio.html', data)

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def perfil(request, nombreUsuario):
    data = {}
    usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
    productos = Producto.getProductosDeUsuario(usuario)
    valoraciones = Valoracion.getValoracionesPerfil(usuario.idUsuario)
    data['usuario'] = usuario
    data['idUsuario'] = usuario.idUsuario
    data['productos'] = productos
    data['valoraciones'] = valoraciones
    if request.session.get('usuario') != None:
        nombreUsuarioLogueado = request.session.get('usuario')
        usuarioLogueado = Usuario.getUsuarioPorNombreUsuario(nombreUsuarioLogueado)
        listado = Listado.getListadoUsuariosFavoritos(usuarioLogueado)
        existeListadoProducto = ListadoProducto.existenListadosIguales(listado, None, usuario)
        if existeListadoProducto:
            data['existeListadoUsuario'] = True
        else:
            data['existeListadoUsuario'] = False
    return render (request, 'perfil.html', data)

def detallesProducto(request, idProducto):
    nombreUsuario = request.session.get('usuario')
    data = {}
    producto = Producto.getProductoPorId(idProducto)
    cat= Producto.getCategoriasDeProducto(idProducto)
    valoraciones = Valoracion.getValoracionesDeProducto(idProducto)
    puntuacion = Valoracion.getPuntuaciónProducto(idProducto)
    if puntuacion == None:
        puntuacion = '-'
    categorias = ", ".join([str(c.idCategoria.nombre) for c in cat if c])
    data['producto'] = producto
    data['categorias'] = categorias
    data['valoraciones'] = valoraciones
    data['puntuacion'] = puntuacion
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        listado = Listado.getListadoProductosFavoritos(usuario)
        existeListadoProducto = ListadoProducto.existenListadosIguales(listado, producto, None)
        if existeListadoProducto:
            data['existeListadoProducto'] = True
        else:
            data['existeListadoProducto'] = False
    return render (request, 'detallesProducto.html', data)

def listadoChats(request):
    data = {}
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        listado = Chat.getChatsPorUsuario(usuario.idUsuario)
        data['chats'] = listado
    
        return render (request, 'listadoChats.html', data)
    else:
        return render (request, 'login.html')

def registroPrestamos(request):
    data = {}
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        prestamos = Prestamo.getRegistroPrestamosPorUsuario(usuario.idUsuario)
        data['prestamos'] = prestamos
    
        return render (request, 'registroPrestamos.html', data)
    else:
        return render (request, 'login.html')
def filtros(request):
    data = {}
    categorias = Categoria.objects.all().order_by('nombre')
    data['categorias'] = categorias
    return render(request, 'filtros.html', data)

def logrosEstadisticas(request):
    return render(request, 'logrosEstadisticas.html')

def crearChat(request, idProducto):
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        producto = Producto.getProductoPorId(idProducto)
        usuarioPropietario = producto.idPropietario
        existeChat = Chat.existeChat(usuarioPropietario, usuario, producto)
        if existeChat:
            return listadoChats(request)
        else : 
            nuevoChat = Chat(idUsuarioArrendador=usuarioPropietario, idUsuarioArrendatario=usuario, idProducto=producto)
            nuevoChat.save()
            return listadoChats(request)
    else:
        return render (request, 'login.html')
    
def estadisticas(request):
    data = {}
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        estadisticas = EstadisticaUsuario.getEstadisticasDeUsuario(usuario)
        data['estadisticas'] = estadisticas

        return render (request, 'estadisticas.html', data)
    else:
        return render (request, 'login.html')
    
def logros(request):
    data = {}
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        completados = LogroUsuario.GetLogrosObtenidosDeUsuario(usuario)
        noCompletados = LogroUsuario.GetLogros_No_ObtenidosDeUsuario(usuario)
        data['completados'] = completados
        data['noCompletados'] = noCompletados

        return render (request, 'logros.html', data)
    else:
        return render (request, 'login.html')
    
def listados(request): 
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        return render (request, 'listados.html')
    else:
        return render (request, 'login.html')
    
def productosFavoritos(request):
    data = {}
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        listadoProductosFavoritos = Listado.getListadoProductosFavoritos(usuario)
        productosFavoritos = ListadoProducto.getListadoItems(listadoProductosFavoritos.idListado)
        data['productosFavoritos'] = productosFavoritos
        return render (request, 'productosFavoritos.html', data)

    else:
        return render (request, 'login.html')
    
def eliminarProductoDeListado(request, idListadoProducto):
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        listadoProducto = ListadoProducto.getListadoProductoPorId(idListadoProducto)
        listado = listadoProducto.idListado
        if listado.idPropietario.idUsuario == usuario.idUsuario :
            listadoProducto.delete()
            return redirect("productosFavoritos")
        else :
            return redirect("productosFavoritos")

    else:
        return render (request, 'login.html')
    
def anadirProductoAFavoritos(request, idProducto) :
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        producto = Producto.getProductoPorId(idProducto)
        listadoProductosFavoritos = Listado.getListadoProductosFavoritos(usuario.idUsuario)
        listadoProducto = ListadoProducto(
            idListado = listadoProductosFavoritos,
            idProducto = producto,
            idUsuario = None,
            fechaAdicion = datetime.datetime.now()
        )
        existenIguales = ListadoProducto.existenListadosIguales(listadoProductosFavoritos.idListado, producto.idProducto, None)
        if existenIguales:
            return redirect("detalles", idProducto=idProducto)
        else:
            listadoProducto.save()
            return redirect("detalles", idProducto=idProducto)

    else:
        return render (request, 'login.html')
    
def usuariosFavoritos(request):
    data = {}
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        listadoUsuariosFavoritos = Listado.getListadoUsuariosFavoritos(usuario)
        usuariosFavoritos = ListadoProducto.getListadoItems(listadoUsuariosFavoritos.idListado)
        data['usuariosFavoritos'] = usuariosFavoritos
        return render (request, 'usuariosFavoritos.html', data)

    else:
        return render (request, 'login.html')
    
def eliminarUsuarioDeListado(request, idListadoProducto):
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        listadoProducto = ListadoProducto.getListadoProductoPorId(idListadoProducto)
        listado = listadoProducto.idListado
        if listado.idPropietario.idUsuario == usuario.idUsuario :
            listadoProducto.delete()
            return redirect("usuariosFavoritos")
        else :
            return redirect("usuariosFavoritos")

    else:
        return render (request, 'login.html')

def anadirUsuarioAFavoritos(request, idUsuario) :
    nombreUsuario = request.session.get('usuario')
    if nombreUsuario != None:
        usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
        usuarioAGuardar = Usuario.getUsuarioPorId(idUsuario)
        listadoUsuariosFavoritos = Listado.getListadoUsuariosFavoritos(usuario.idUsuario)
        listadoProducto = ListadoProducto(
            idListado = listadoUsuariosFavoritos,
            idProducto = None,
            idUsuario = usuarioAGuardar,
            fechaAdicion = datetime.datetime.now()
        )
        existenIguales = ListadoProducto.existenListadosIguales(listadoUsuariosFavoritos.idListado, None, usuarioAGuardar.idUsuario)
        if existenIguales:
            return redirect("perfil", nombreUsuario=usuarioAGuardar.nombreUsuario)
        else:
            listadoProducto.save()
            return redirect("perfil", nombreUsuario=usuarioAGuardar.nombreUsuario)

    else:
        return render (request, 'login.html')