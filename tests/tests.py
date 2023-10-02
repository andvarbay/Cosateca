from urllib.parse import urlencode
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from CosatecaApp.models import *
from cosateca import settings

@pytest.fixture
def client():
    return Client()

# ===================REGISTER=====================
@pytest.fixture
def register_data_pass():
    return {
        'nombre': 'usu',
        'apellidos': 'ario',
        'correo': 'jtest@test.com',
        'ubicacion': 'test',
        'nombreUsuario': 'test_user',
        'contrasena': 'test123',
        'contrasena2': 'test123',
        'fotoPerfil': ''
    }
@pytest.fixture
def register_data_fail():
    return {
        'nombre': '',
        'apellidos': '',
        'correo': 'a@a',
        'ubicacion': 'test',
        'nombreUsuario': 'test_user',
        'contrasena': 'tes',
        'contrasena2': 'test123',
        'fotoPerfil': ''
    }

@pytest.mark.django_db
def test_register_success(client, register_data_pass):
    response = client.post(reverse('register'), data=register_data_pass)

    assert response.status_code == 302
    assert response.url == reverse('login')

    assert Usuario.objects.filter(nombreUsuario=register_data_pass['nombreUsuario']).exists()

    usuario = Usuario.objects.get(nombreUsuario=register_data_pass['nombreUsuario'])
    assert usuario.nombre == register_data_pass['nombre']
    assert usuario.apellidos == register_data_pass['apellidos']
    assert usuario.correo == register_data_pass['correo']
    assert usuario.ubicacion == register_data_pass['ubicacion']
    assert usuario.rol == 'usuario'

@pytest.mark.django_db
def test_register_fail(client, register_data_fail):
    response = client.post(reverse('register'), data=register_data_fail)


    assert response.status_code == 200 
    assert b'Introduce tu nombre.' in response.content
    assert b'Introduce tus apellidos.' in response.content
    assert b'Los apellidos deben tener al menos 3 caracteres.' in response.content
    assert 'La contraseña debe tener al menos 5 caracteres.'.encode('utf-8') in response.content
    assert 'Las contraseñas deben ser iguales.'.encode('utf-8') in response.content
    assert 'El correo debe tener más de 5 caracteres.'.encode('utf-8') in response.content
    assert b'Introduce tu nombre.' in response.content
    assert not Usuario.objects.filter(nombreUsuario=register_data_fail['nombreUsuario']).exists()

# ===================LOGIN=====================
@pytest.fixture
def test_user(client):
    client = Client()
    data_usuario = {
            'nombre':'usu',
            'apellidos':'ario',
            'correo':'test@test',
            'ubicacion':'test',
            'nombreUsuario':'test',
            'contrasena':'ContrasenaTest',
            'contrasena2':'ContrasenaTest',
            'fotoPerfil':''
    }
    response = client.post(reverse('register'), data=data_usuario)
    assert response.status_code == 302

@pytest.mark.django_db
def test_login_pass(client, test_user):
    response = client.post(reverse('login'), data={'nombreUsuario': 'test', 'contrasena': 'ContrasenaTest'})
    assert response.status_code == 302

@pytest.mark.django_db
def test_login_fail_doesnt_exist(client, test_user):
    usuario = test_user
    response = client.post(reverse('login'), data={'nombreUsuario': 'teasdasdsast', 'contrasena': 'ContrasenaTest'})
    assert response.status_code == 200
    assert b'Nombre de usuario no existe' in response.content

@pytest.mark.django_db
def test_login_wrong_password(client, test_user):
    usuario = test_user
    response = client.post(reverse('login'), data={'nombreUsuario': 'test', 'contrasena': 'Contasdasadt'})
    assert response.status_code == 200
    assert 'Contraseña incorrecta'.encode('utf-8') in response.content

# ===================PERFIL=====================
@pytest.fixture
def logged_in_client(client, test_user):
    usuario = test_user
    client = Client()
    login_data = {
        'nombreUsuario': 'test',
        'contrasena': 'ContrasenaTest'  
    }
    response = client.post(reverse('login'), data=login_data)
    assert response.status_code == 302
    return client

@pytest.mark.django_db
def test_perfil_propio(logged_in_client, test_user):
    usuario = test_user
    response = logged_in_client.get(reverse('perfil', kwargs={'nombreUsuario': 'test'}))
    assert response.status_code == 200
    assert b'PRODUCTOS DE test' in response.content
    assert b'EDITAR PERFIL' in response.content
    assert 'SOLICITUDES DE PRÉSTAMO'.encode('utf-8') in response.content
    assert 'REGISTRO DE PRÉSTAMOS'.encode('utf-8') in response.content
    assert b'ELIMINAR CUENTA' in response.content

@pytest.mark.django_db
def test_perfil_ajeno(logged_in_client):
    response = logged_in_client.get(reverse('perfil', kwargs={'nombreUsuario': 'pablester'}))
    assert response.status_code == 200
    assert b'PRODUCTOS DE pablester' in response.content
    assert b'VALORAR' in response.content
    assert b'REPORTAR' in response.content
    

# ===================CREATE PRODUCTO=====================
@pytest.fixture
def product_data():
    return {
        'nombre': 'producto',
        'descripcion': 'descripcion_de_producto',
        'fotoProducto': ''
    }

@pytest.mark.django_db
def test_crear_producto_success(logged_in_client, product_data):
    response = logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    assert response.status_code == 302
    assert Producto.objects.get(nombre='producto')
    p = Producto.objects.get(nombre='producto')
    assert p.nombre == 'producto'
    assert p.descripcion == 'descripcion_de_producto'
    assert p.fotoProducto == None

# ===================DETALLES PRODUCTO=====================

@pytest.mark.django_db
def test_ver_producto_propio(logged_in_client, product_data):
    logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    p = Producto.objects.get(nombre='producto')
    response = logged_in_client.get(reverse('detalles', kwargs={'idProducto': p.idProducto}))
    assert response.status_code == 200
    assert 'AÑADIR A...'.encode('utf-8') in response.content
    assert b'DE: test' in response.content
    assert b'descripcion_de_producto' in response.content
    assert b'VALORAR' not in response.content
    assert b'REPORTAR' not in response.content
    
@pytest.mark.django_db
def test_ver_producto_ajeno(client, logged_in_client, product_data):
    logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    p = Producto.objects.get(nombre='producto')
    response = client.get(reverse('detalles', kwargs={'idProducto': p.idProducto}))
    assert response.status_code == 200
    assert 'AÑADIR A...'.encode('utf-8') in response.content
    assert b'DE: test' in response.content
    assert b'descripcion_de_producto' in response.content
    assert b'VALORAR' in response.content
    assert b'REPORTAR' in response.content

# ===================VALORAR PRODUCTO=====================
@pytest.mark.django_db
def test_valorar_producto_ajeno(client, logged_in_client, product_data):
    logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    p = Producto.objects.get(nombre='producto')
    par = 'p_'+str(p.idProducto )
    parametros = {'id': par}   
    url = '/realizarValoracion/?' + urlencode(parametros)
    response = client.post(reverse('login'), data={'nombreUsuario': 'pablester', 'contrasena': 'pablester123'})
    assert response.status_code == 302
    response = client.get(url)
    assert response.status_code == 200
    assert b'VALORAR producto' in response.content

# ===================REPORTAR PRODUCTO=====================

@pytest.mark.django_db
def test_reportar_producto_ajeno(client, logged_in_client, product_data):
    logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    p = Producto.objects.get(nombre='producto')
    param = 'p_'+str(p.idProducto )
    parametros = {'id': param}   
    url = '/realizarReporte/?' + urlencode(parametros)
    response = client.post(reverse('login'), data={'nombreUsuario': 'pablester', 'contrasena': 'pablester123'})
    assert response.status_code == 302
    response = client.get(url)
    assert response.status_code == 200
    assert b'Reportar' in response.content
    assert b'producto' in response.content
    assert b'MOTIVOS DEL REPORTE' in response.content
    response = client.post(url, data={'descripcion': ''})
    assert response.status_code == 200
    response = client.post(url, data={'descripcion': 'Este producto no debería estar en esta aplicación.'})
    assert response.status_code == 200


# ===================EDITAR PRODUCTO=====================
@pytest.mark.django_db
def test_editar_producto_pass(logged_in_client,product_data):
    response = logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    assert response.status_code == 302
    p =  Producto.objects.get(nombre='producto')
    param = p.idProducto
    parametros = {'idProducto': param}   
    
    url = reverse('editarProducto')+'?' + urlencode(parametros)

    response = logged_in_client.get(url)
    assert response.status_code == 200
    assert b'descripcion_de_producto' in response.content
    response = logged_in_client.post(url,{
                                         'idProducto': p.idProducto,
                                         'nombre': 'producto_cambio',
                                         'descripcion': 'descripcion_cambiada',
                                         })

    assert response.status_code == 302
    response = logged_in_client.get(reverse('detalles', kwargs={'idProducto': p.idProducto}))
    p =Producto.objects.get(idProducto = p.idProducto)
    assert p.nombre == 'producto_cambio'
    assert p.descripcion == 'descripcion_cambiada'

# ===================BORRAR PERFIL=====================
@pytest.mark.django_db
def test_borrar_perfil(logged_in_client):
    usuarios_antes = Usuario.objects.all().count()
    url = reverse('borrarPerfil')
    response = logged_in_client.post(url, {'respuesta': 'confirmar'})
    usuarios_despues = Usuario.objects.all().count()
    assert usuarios_antes - usuarios_despues == 1
    assert not Usuario.objects.filter(nombreUsuario='test').exists()

# ===================EDITAR PERFIL=====================

@pytest.mark.django_db
def test_editar_perfil_pass(logged_in_client,product_data):
    response = logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    assert response.status_code == 302
    url = reverse('editarPerfil')
    usu1 = Usuario.getUsuarioPorNombreUsuario('test')
    usuId = usu1.idUsuario
    response = logged_in_client.post(url, {'nombre': 'nom',
                                           'apellidos': 'ape',
                                           'correo': 'tes@tes',
                                           'ubicacion': 'ubi',
                                           'nombreUsuario':'test2',
                                           'contrasena': '',
                                           'contrasenaNueva': '',
                                           'contrasenaNueva2': '',
                                           'fotoPerfil': ''
                                           })
    assert response.status_code == 302
    usu2 = Usuario.getUsuarioPorId(usuId)
    assert usu1.apellidos != usu2.apellidos
    assert usu1.correo != usu2.correo
    assert usu1.ubicacion != usu2.ubicacion
    assert usu1.nombreUsuario != usu2.nombreUsuario
    

@pytest.mark.django_db
def test_editar_perfil_fail(logged_in_client,product_data):
    response = logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    assert response.status_code == 302
    url = reverse('editarPerfil')
    response = logged_in_client.post(url, {'nombre': 'no',
                                           'apellidos': 'ae',
                                           'correo': 'ts@t',
                                           'ubicacion': 'ubi',
                                           'nombreUsuario':'pablester',
                                           'contrasena': 'aad',
                                           'contrasenaNueva': 'asd',
                                           'contrasenaNueva2': 'aaa',
                                           'fotoPerfil': ''
                                           })
    assert response.status_code == 200
    assert b'El nombre debe tener al menos 3 caracteres.' in response.content
    assert b'Los apellidos deben tener al menos 3 caracteres.' in response.content
    assert 'Contraseña actual incorrecta'.encode('utf-8') in response.content
    assert 'La contraseña debe tener al menos 5 caracteres.'.encode('utf-8') in response.content
    assert 'Las contraseñas deben ser iguales.'.encode('utf-8') in response.content
    assert 'El correo debe tener más de 5 caracteres.'.encode('utf-8') in response.content
    assert 'Nombre de usuario ya registrado.'.encode('utf-8') in response.content
    

# ===================PEDIR PRESTAMO=====================
@pytest.mark.django_db
def test_pedir_prestamo(client, logged_in_client, product_data):
    logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    p = Producto.objects.get(nombre='producto')
    par = 'p_'+str(p.idProducto )
    parametros = {'id': par}   
    url = '/pedirPrestamo/?' + urlencode(parametros)
    client = Client()
    response = client.post(reverse('login'), data={'nombreUsuario': 'pablester', 'contrasena': 'pablester123'})
    assert response.status_code == 302
    response = client.get(url)
    assert response.status_code == 200
    assert b'Solicitar' in response.content
    assert b'producto' in response.content
    assert b'test' in response.content
    response = client.post(url, {
        'fechaInicio':'31/10/2024',
        'fechaFin':'30/11/2024',
        'condiciones': 'Lo necesito para obras en mi garaje'
    })
    assert response.status_code == 200
    arrendatario = Usuario.objects.get(nombreUsuario='pablester')
    assert Prestamo.objects.filter(idArrendatario=arrendatario, idProducto=p).exists()


# ===================LOGROS Y ESTADISTICAS=====================

@pytest.mark.django_db
def test_menu_logros_estadisticas(logged_in_client):
    response = logged_in_client.get(reverse('logrosEstadisticasMenu'))
    assert response.status_code == 200
    assert 'LOGROS'.encode('utf-8') in response.content
    assert 'ESTADÍSTICAS'.encode('utf-8') in response.content


@pytest.mark.django_db
def test_logros(logged_in_client):
    response = logged_in_client.get(reverse('logros'))
    assert response.status_code == 200
    assert 'LOGROS'.encode('utf-8') in response.content
    assert 'Bienvenido a Cosateca'.encode('utf-8') in response.content
    assert 'Proveedor novato'.encode('utf-8') in response.content
    assert 'Proveedor intermedio'.encode('utf-8') in response.content
    assert 'Proveedor experto'.encode('utf-8') in response.content
    assert 'Repartiendo amor'.encode('utf-8') in response.content
    assert 'Libertad de expresión'.encode('utf-8') in response.content
    assert 'Valorando el mercado'.encode('utf-8') in response.content
    assert 'El juez'.encode('utf-8') in response.content
    assert 'En el punto de mira'.encode('utf-8') in response.content
    assert 'La vieja confiable'.encode('utf-8') in response.content
    assert 'Solo Dios puede juzgarme'.encode('utf-8') in response.content
    assert 'Negocio local'.encode('utf-8') in response.content
    assert 'Hombre de negocios'.encode('utf-8') in response.content
    assert 'Usuario de honor'.encode('utf-8') in response.content
    assert 'Arrendador primerizo'.encode('utf-8') in response.content
    assert 'Arrendador ocasional'.encode('utf-8') in response.content
    assert 'Arrendando que es gerundio'.encode('utf-8') in response.content
    assert 'Arrendatario primerizo'.encode('utf-8') in response.content
    assert 'Arrendatario ocasional'.encode('utf-8') in response.content
    assert 'Arrendatando que es gerundio'.encode('utf-8') in response.content
    usu = Usuario.getUsuarioPorNombreUsuario('test')
    logro = Logro.GetLogroPorNombre('Bienvenido a Cosateca')
    assert LogroUsuario.objects.get(idLogro = logro, idUsuario = usu)


@pytest.mark.django_db
def test_logros_subir_productos(logged_in_client, product_data):
    estad = Estadistica.getEstadisticaPorNombre('Productos subidos')
    usu = Usuario.getUsuarioPorNombreUsuario('test')
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 0
    response = logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    assert response.status_code == 302
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 1
    logro1 = Logro.GetLogroPorNombre('Proveedor novato')
    logro5 = Logro.GetLogroPorNombre('Proveedor intermedio')
    logro10 = Logro.GetLogroPorNombre('Proveedor experto')
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert not LogroUsuario.objects.filter(idLogro=logro5, idUsuario=usu).exists()
    assert not LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()
    for i in [1,2,3,4]:
        response = logged_in_client.post(reverse('nuevoProducto'), data = product_data)
        assert response.status_code == 302
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 5
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert LogroUsuario.objects.get(idLogro = logro5, idUsuario = usu)
    assert not LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()
    for i in [1,2,3,4,5]:
        response = logged_in_client.post(reverse('nuevoProducto'), data = product_data)
        assert response.status_code == 302
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 10
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert LogroUsuario.objects.get(idLogro = logro5, idUsuario = usu)
    assert LogroUsuario.objects.get(idLogro = logro10, idUsuario = usu)


@pytest.mark.django_db
def test_logros_realizar_valoraciones(logged_in_client):
    estad = Estadistica.getEstadisticaPorNombre('Comentarios publicados')
    usu = Usuario.getUsuarioPorNombreUsuario('test')
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 0
    logro1 = Logro.GetLogroPorNombre('Libertad de expresión')
    logro5 = Logro.GetLogroPorNombre('Valorando el mercado')
    logro10 = Logro.GetLogroPorNombre('El juez')

    p = Producto.objects.get(idProducto=1)
    par = 'p_'+str(p.idProducto )
    parametros = {'id': par}   
    url = '/realizarValoracion/?' + urlencode(parametros)
    logged_in_client.post(url, data={
                                        'puntuacion': 4,
                                        'comentario': 'Me ha gustado mucho',
                                        'idEmisor': usu.nombreUsuario
                                    })
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor==1
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert not LogroUsuario.objects.filter(idLogro=logro5, idUsuario=usu).exists()
    assert not LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()

    val = Valoracion.objects.get(idEmisor=usu,idProducto=p)
    val.delete()
    for i in [1,2,3,4]:
        logged_in_client.post(url, data={
                                            'puntuacion': 4,
                                            'comentario': 'Me ha gustado mucho',
                                            'idEmisor': usu.nombreUsuario
                                        })
        val = Valoracion.objects.get(idEmisor=usu,idProducto=p)
        val.delete()

    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 5
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert LogroUsuario.objects.filter(idLogro=logro5, idUsuario=usu).exists()
    assert not LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()
    for i in [1,2,3,4,5]:
        logged_in_client.post(url, data={
                                            'puntuacion': 4,
                                            'comentario': 'Me ha gustado mucho',
                                            'idEmisor': usu.nombreUsuario
                                        })
        val = Valoracion.objects.get(idEmisor=usu,idProducto=p)
        val.delete()

    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 10
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert LogroUsuario.objects.filter(idLogro=logro5, idUsuario=usu).exists()
    assert LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()

@pytest.mark.django_db
def test_logros_recibir_valoraciones(client, logged_in_client, product_data):
    client = Client()
    response = client.post(reverse('login'), {
                'nombreUsuario': 'pablester',
                'contrasena':'pablester123'
                                   })
    
    assert response.status_code == 302
    estad = Estadistica.getEstadisticaPorNombre('Valoraciones recibidas')
    usu = Usuario.getUsuarioPorNombreUsuario('test')
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 0
    logro1 = Logro.GetLogroPorNombre('En el punto de mira')
    logro5 = Logro.GetLogroPorNombre('La vieja confiable')
    logro10 = Logro.GetLogroPorNombre('Solo Dios puede juzgarme')

    response = logged_in_client.post(reverse('nuevoProducto'), data= product_data)
    assert response.status_code == 302
    pablester = Usuario.getUsuarioPorNombreUsuario('pablester')
    p = Producto.objects.get(nombre='producto')
    par = 'p_'+str(p.idProducto)
    parametros = {'id': par}   
    url = '/realizarValoracion/?' + urlencode(parametros)
    client.post(url, data={
                                        'puntuacion': 4,
                                        'comentario': 'Me ha gustado mucho',
                                        'idEmisor': pablester.nombreUsuario
                                    })
    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor==1
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert not LogroUsuario.objects.filter(idLogro=logro5, idUsuario=usu).exists()
    assert not LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()

    val = Valoracion.objects.get(idEmisor=pablester,idProducto=p)
    val.delete()
    for i in [1,2,3,4]:
        client.post(url, data={
                                            'puntuacion': 4,
                                            'comentario': 'Me ha gustado mucho',
                                            'idEmisor': pablester.nombreUsuario
                                        })
        val = Valoracion.objects.get(idEmisor=pablester,idProducto=p)
        val.delete()

    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 5
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert LogroUsuario.objects.filter(idLogro=logro5, idUsuario=usu).exists()
    assert not LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()
    for i in [1,2,3,4,5]:
        client.post(url, data={
                                            'puntuacion': 4,
                                            'comentario': 'Me ha gustado mucho',
                                            'idEmisor': pablester.nombreUsuario
                                        })
        val = Valoracion.objects.get(idEmisor=pablester,idProducto=p)
        val.delete()

    estadusu = EstadisticaUsuario.objects.get(idEstadistica=estad,idUsuario=usu)
    assert estadusu.valor == 10
    assert LogroUsuario.objects.get(idLogro = logro1, idUsuario = usu)
    assert LogroUsuario.objects.filter(idLogro=logro5, idUsuario=usu).exists()
    assert LogroUsuario.objects.filter(idLogro=logro10, idUsuario=usu).exists()


@pytest.mark.django_db
def test_logros_participar_prestamos(client, logged_in_client, product_data):
    logged_in_client.post(reverse('nuevoProducto'), data = product_data)
    client = Client()
    p = Producto.objects.get(nombre='producto')
    par = 'p_'+str(p.idProducto )
    parametros = {'id': par}   
    url = '/pedirPrestamo/?' + urlencode(parametros)
    response = client.post(reverse('login'), data={'nombreUsuario': 'carlosv', 'contrasena': 'sutremendalteza123'})
    assert response.status_code == 302
    response = client.get(url)
    assert response.status_code == 200
    assert b'Solicitar' in response.content
    assert b'producto' in response.content
    assert b'test' in response.content
    response = client.post(url, {
        'fechaInicio':'31/10/2024',
        'fechaFin':'30/11/2024',
        'condiciones': 'Lo necesito para obras en mi garaje'
    })
    assert response.status_code == 200
    arrendatario = Usuario.objects.get(nombreUsuario='carlosv')
    assert Prestamo.objects.filter(idArrendatario=arrendatario, idProducto=p).exists()
    prestamo =  Prestamo.objects.get(idArrendatario=arrendatario, idProducto=p)

    prestamos_realizados = Estadistica.getEstadisticaPorNombre('Préstamos realizados')
    prestamos_arrendador = Estadistica.getEstadisticaPorNombre('Préstamos como arrendador')
    prestamos_arrendatario = Estadistica.getEstadisticaPorNombre('Préstamos como arrendatario')
    usutest = Usuario.getUsuarioPorNombreUsuario('test')
    usucarlos = Usuario.getUsuarioPorNombreUsuario('carlosv')
    
    logro1_realizados = Logro.GetLogroPorNombre('Negocio local')
    logro5_realizados = Logro.GetLogroPorNombre('Hombre de negocios')
    logro10_realizados = Logro.GetLogroPorNombre('Usuario de honor')
    logro1_arrendador = Logro.GetLogroPorNombre('Arrendador primerizo')
    logro5_arrendador = Logro.GetLogroPorNombre('Arrendador ocasional')
    logro10_arrendador = Logro.GetLogroPorNombre('Arrendando que es gerundio')
    logro1_arrendatario = Logro.GetLogroPorNombre('Arrendatario primerizo')
    logro5_arrendatario = Logro.GetLogroPorNombre('Arrendatario ocasional')
    logro10_arrendatario = Logro.GetLogroPorNombre('Arrendatando que es gerundio')



    est_realizados_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usutest)
    est_arrendador_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usutest)
    est_arrendatario_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usutest)
    est_realizados_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usucarlos)
    est_arrendador_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usucarlos)
    est_arrendatario_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usucarlos)
    
    est_arrendatario_carlos.valor = 0
    est_arrendatario_carlos.save()

    assert est_realizados_test.valor == 0
    assert est_arrendador_test.valor == 0
    assert est_arrendatario_test.valor == 0
    assert est_realizados_carlos.valor == 0
    assert est_arrendador_carlos.valor == 0
    assert est_arrendatario_carlos.valor == 0

    prestamo =  Prestamo.objects.get(idArrendatario=arrendatario, idProducto=p)
    logged_in_client.post(reverse('solicitudesPrestamo'), {
                                    'idPrestamo': prestamo.idPrestamo,
                                    'respuesta': 'aceptar'
                                                            })
    prestamo =  Prestamo.objects.get(idArrendatario=arrendatario, idProducto=p)

    assert prestamo.estado == 'Aceptado'
    prestamo =  Prestamo.objects.get(idArrendatario=arrendatario, idProducto=p)
    prestamo.estado = 'Pendiente'
    Prestamo.guardarPrestamo(prestamo)
    prestamo =  Prestamo.objects.get(idArrendatario=arrendatario, idProducto=p)


    est_realizados_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usutest)
    est_arrendador_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usutest)
    est_arrendatario_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usutest)
    est_realizados_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usucarlos)
    est_arrendador_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usucarlos)
    est_arrendatario_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usucarlos)
    
    assert est_realizados_test.valor == 1
    assert est_arrendador_test.valor == 1
    assert est_realizados_carlos.valor == 1
    assert est_arrendatario_carlos.valor == 1
    
    assert LogroUsuario.objects.get(idLogro = logro1_realizados, idUsuario = usucarlos)
    assert not LogroUsuario.objects.filter(idLogro = logro5_realizados, idUsuario = usucarlos).exists()
    assert not LogroUsuario.objects.filter(idLogro = logro10_realizados, idUsuario = usucarlos).exists()
    assert LogroUsuario.objects.get(idLogro = logro1_realizados, idUsuario = usutest)
    assert not LogroUsuario.objects.filter(idLogro = logro5_realizados, idUsuario = usutest).exists()
    assert not LogroUsuario.objects.filter(idLogro = logro10_realizados, idUsuario = usutest).exists()

    assert LogroUsuario.objects.get(idLogro = logro1_arrendador, idUsuario = usutest)
    assert not LogroUsuario.objects.filter(idLogro = logro5_arrendador, idUsuario = usutest).exists()
    assert not LogroUsuario.objects.filter(idLogro = logro10_arrendador, idUsuario = usutest).exists()
    assert LogroUsuario.objects.get(idLogro = logro1_arrendatario, idUsuario = usucarlos)
    assert not LogroUsuario.objects.filter(idLogro = logro5_arrendatario, idUsuario = usucarlos).exists()
    assert not LogroUsuario.objects.filter(idLogro = logro10_arrendatario, idUsuario = usucarlos).exists()

    for i in [1,2,3,4]:
        logged_in_client.post(reverse('solicitudesPrestamo'), {
                                                                'idPrestamo': prestamo.idPrestamo,
                                                                'respuesta': 'aceptar'
                                                                })
        prestamo =  Prestamo.objects.get(idArrendatario=arrendatario, idProducto=p)
        assert prestamo.estado == 'Aceptado'
        prestamo.estado = 'Pendiente'
        Prestamo.guardarPrestamo(prestamo)
    
    est_realizados_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usutest)
    est_arrendador_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usutest)
    est_arrendatario_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usutest)
    est_realizados_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usucarlos)
    est_arrendador_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usucarlos)
    est_arrendatario_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usucarlos)
    
    assert est_realizados_test.valor == 5
    assert est_arrendador_test.valor == 5
    assert est_realizados_carlos.valor == 5
    assert est_arrendatario_carlos.valor == 5
    
    assert LogroUsuario.objects.get(idLogro = logro1_realizados, idUsuario = usucarlos)
    assert LogroUsuario.objects.filter(idLogro = logro5_realizados, idUsuario = usucarlos)
    assert not LogroUsuario.objects.filter(idLogro = logro10_realizados, idUsuario = usucarlos).exists()
    assert LogroUsuario.objects.get(idLogro = logro1_realizados, idUsuario = usutest)
    assert LogroUsuario.objects.filter(idLogro = logro5_realizados, idUsuario = usutest)
    assert not LogroUsuario.objects.filter(idLogro = logro10_realizados, idUsuario = usutest).exists()


    assert LogroUsuario.objects.get(idLogro = logro1_arrendador, idUsuario = usutest)
    assert LogroUsuario.objects.filter(idLogro = logro5_arrendador, idUsuario = usutest)
    assert not LogroUsuario.objects.filter(idLogro = logro10_arrendador, idUsuario = usutest).exists()
    assert LogroUsuario.objects.get(idLogro = logro1_arrendatario, idUsuario = usucarlos)
    assert LogroUsuario.objects.filter(idLogro = logro5_arrendatario, idUsuario = usucarlos)
    assert not LogroUsuario.objects.filter(idLogro = logro10_arrendatario, idUsuario = usucarlos).exists()
    
    for i in [1,2,3,4,5]:
        logged_in_client.post(reverse('solicitudesPrestamo'), {
                                                                'idPrestamo': prestamo.idPrestamo,
                                                                'respuesta': 'aceptar'
                                                                })
        prestamo =  Prestamo.objects.get(idArrendatario=arrendatario, idProducto=p)
        assert prestamo.estado == 'Aceptado'
        prestamo.estado = 'Pendiente'
        Prestamo.guardarPrestamo(prestamo)
    
    est_realizados_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usutest)
    est_arrendador_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usutest)
    est_arrendatario_test = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usutest)
    est_realizados_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_realizados,usucarlos)
    est_arrendador_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendador,usucarlos)
    est_arrendatario_carlos = EstadisticaUsuario.getEstadisticaUsuario(prestamos_arrendatario,usucarlos)
    
    assert est_realizados_test.valor == 10
    assert est_arrendador_test.valor == 10
    assert est_realizados_carlos.valor == 10
    assert est_arrendatario_carlos.valor == 10
    
    assert LogroUsuario.objects.get(idLogro = logro1_realizados, idUsuario = usucarlos)
    assert LogroUsuario.objects.filter(idLogro = logro5_realizados, idUsuario = usucarlos)
    assert LogroUsuario.objects.filter(idLogro = logro10_realizados, idUsuario = usucarlos)
    assert LogroUsuario.objects.get(idLogro = logro1_realizados, idUsuario = usutest)
    assert LogroUsuario.objects.filter(idLogro = logro5_realizados, idUsuario = usutest)
    assert LogroUsuario.objects.filter(idLogro = logro10_realizados, idUsuario = usutest)


    assert LogroUsuario.objects.get(idLogro = logro1_arrendador, idUsuario = usutest)
    assert LogroUsuario.objects.filter(idLogro = logro5_arrendador, idUsuario = usutest)
    assert LogroUsuario.objects.filter(idLogro = logro10_arrendador, idUsuario = usutest)
    assert LogroUsuario.objects.get(idLogro = logro1_arrendatario, idUsuario = usucarlos)
    assert LogroUsuario.objects.filter(idLogro = logro5_arrendatario, idUsuario = usucarlos)
    assert LogroUsuario.objects.filter(idLogro = logro10_arrendatario, idUsuario = usucarlos)
    