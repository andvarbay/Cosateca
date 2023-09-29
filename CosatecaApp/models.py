import json
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix
from minio import Minio
from django.db.models import Avg
from django.db.models import Q

from cosateca.settings import SECRETS

# Create your models here.
client = Minio(
                SECRETS['MINIO_ENDPOINT'],
                access_key = SECRETS['MINIO_ACCESS_KEY'],
                secret_key = SECRETS['MINIO_SECRET_KEY']
            )

class PrivateAttachment(models.Model):
    file = models.FileField(verbose_name="Object Upload",
                            storage=MinioBackend(bucket_name='django-backend-dev-public'),
                            upload_to=iso_date_prefix,)
    

    def __str__(self):
        return str(self.file)
        
    def nuevaFoto(self):
        self.save()

    @staticmethod
    def getFoto(file):
        try:
            return PrivateAttachment.objects.get(file = file)
        except:
            return False


class Categoria(models.Model):
    idCategoria = models.AutoField(db_column='idCategoria', primary_key=True)  
    nombre = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'categoria'

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def getCategoriaPorId(idCategoria):
        try:
            return Categoria.objects.get(idCategoria = idCategoria)
        except:
            return False
        
    @staticmethod
    def getCategoriaPorNombre(nombre):
        try:
            return Categoria.objects.get(nombre = nombre)
        except:
            return False

class Chat(models.Model):
    idChat = models.AutoField(db_column='idChat', primary_key=True) 
    idUsuarioArrendador = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuarioArrendador')  
    idUsuarioArrendatario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuarioArrendatario', related_name='chat_idusuarioarrendatario_set')  # Field name made lowercase.
    idProducto = models.ForeignKey('Producto', models.CASCADE, db_column='idProducto')  

    class Meta:
        managed = False
        db_table = 'chat'
    
    def __str__(self):
        return 'CHAT ' + str(self.idChat) + '. USUARIOS: ' + str(self.idUsuarioArrendador.nombreUsuario) + ' y ' + str(self.idUsuarioArrendatario.nombreUsuario) + '. PRODUCTO: ' + str(self.idProducto.nombre)

    @staticmethod
    def getChatsPorUsuario(idUsuario):
        try:
            chatsArrendador =  Chat.objects.filter(idUsuarioArrendador=idUsuario)
            try: 
                chatsArrendatario = Chat.objects.filter(idUsuarioArrendatario=idUsuario)
                return chatsArrendador | chatsArrendatario
            except:
                return chatsArrendador
        except:
            return []
        
    @staticmethod
    def getChatPorId(idChat):
        try:
            return Chat.objects.get(idChat=idChat)
        except:
            return False
        
    @staticmethod
    def existeChat(idUsuarioArrendador, idUsuarioArrendatario, idProducto):
        try:
            chat = Chat.objects.get(idUsuarioArrendador=idUsuarioArrendador, idUsuarioArrendatario=idUsuarioArrendatario, idProducto=idProducto)
            if chat :
                return True
            else : 
                return False
        except:
            return False


class Estadistica(models.Model):
    idEstadistica = models.AutoField(db_column='idEstadistica', primary_key=True) 
    nombre = models.CharField(blank=True, null=True, max_length=40)
    descripcion = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'estadistica'
    
    def __str__(self):
        return self.nombre

    @staticmethod
    def getTodasEstadisticas():
        return Estadistica.objects.all()
    
    def getEstadisticaPorNombre(nombre):
        return Estadistica.objects.get(nombre=nombre)

class EstadisticaUsuario(models.Model):
    idEstadisticaUsuario = models.AutoField(db_column='idEstadisticaUsuario', primary_key=True)  
    idEstadistica = models.ForeignKey(Estadistica, models.CASCADE, db_column='idEstadistica')  
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario') 
    valor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estadisticausuario'

    def __str__(self):
        return str(self.idEstadisticaUsuario) + ': ' + str(self.idEstadistica) + ' de ' + str(self.idUsuario.nombreUsuario) + ': ' + str(self.valor)

    @staticmethod
    def getEstadisticaUsuario(idEstadistica, idUsuario):
        return EstadisticaUsuario.objects.get(idEstadistica = idEstadistica, idUsuario = idUsuario)
    
    @staticmethod
    def getEstadisticasDeUsuario(idUsuario):
        return EstadisticaUsuario.objects.filter(idUsuario = idUsuario)

class Listado(models.Model):
    idListado = models.AutoField(db_column='idListado', primary_key=True)  
    nombre = models.CharField(max_length=20)
    idPropietario = models.ForeignKey('Usuario', models.CASCADE, db_column='idPropietario') 

    class Meta:
        managed = False
        db_table = 'listado'

    def __str__(self):
        return self.nombre + ' de ' + str(self.idPropietario)
    
    @staticmethod
    def getListasPersonalidazas(idUsuario):
        favoritos=["Productos Favoritos", "Usuarios Favoritos"]
        return Listado.objects.filter(idPropietario=idUsuario).exclude(nombre__in=favoritos)

    @staticmethod
    def getListadoProductosFavoritos(idUsuario):
        return Listado.objects.get(idPropietario = idUsuario, nombre="Productos Favoritos")
    
    @staticmethod
    def getListadoPorId(idListado):
        return Listado.objects.get(idListado = idListado)
    
    @staticmethod
    def getListadoUsuariosFavoritos(idUsuario):
        return Listado.objects.get(idPropietario = idUsuario, nombre="Usuarios Favoritos")
    
class ListadoProducto(models.Model):
    idListadoProducto = models.AutoField(db_column='idListadoProducto', primary_key=True) 
    idListado = models.ForeignKey('Listado', models.CASCADE, db_column='idListado')  
    idProducto = models.ForeignKey('Producto', models.CASCADE, db_column='idProducto', null=True, blank=True) 
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario', null=True, blank=True) 
    fechaAdicion = models.DateTimeField(db_column='fechaAdicion') 

    class Meta:
        managed = False
        db_table = 'listadoproducto'

    def __str__(self):
        return str(self.idListadoProducto) + ': ' + str(self.idListado)
    
    @staticmethod
    def getListadoItems(idListado):
        return ListadoProducto.objects.filter(idListado = idListado)
    
    @staticmethod
    def getListadoProductoPorId(idListadoProducto):
        return ListadoProducto.objects.get(idListadoProducto = idListadoProducto)
    
    @staticmethod
    def existenListadosIguales(idListado, idProducto, idUsuario):
        try:
            return ListadoProducto.objects.get(idListado = idListado, idProducto=idProducto, idUsuario=idUsuario)
        except:
            return False
            
    

class Logro(models.Model):
    idLogro = models.AutoField(db_column='idLogro', primary_key=True) 
    nombre = models.CharField(blank=True, null=True, max_length=40)
    descripcion = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'logro'

    def __str__(self):
        return self.nombre
    @staticmethod
    def GetLogroPorNombre(nombre):
        return Logro.objects.get(nombre = nombre)


class LogroUsuario(models.Model):
    idLogroUsuario = models.AutoField(db_column='idLogroUsuario', primary_key=True) 
    idLogro = models.ForeignKey('Logro', models.CASCADE, db_column='idLogro')  
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario') 
    fechaObtencion = models.DateTimeField(db_column='fechaObtencion') 

    class Meta:
        managed = False
        db_table = 'logrousuario'

    def __str__(self):
        return str(self.idLogroUsuario) + ': ' + str(self.idLogro) + ' - ' + str(self.idUsuario.nombreUsuario)
    
    def GetLogrosObtenidosDeUsuario(idUsuario):
        return LogroUsuario.objects.filter(idUsuario = idUsuario).order_by('idLogro')
    
    def GetLogros_No_ObtenidosDeUsuario(idUsuario):
        logrosObtenidos = LogroUsuario.objects.filter(idUsuario = idUsuario).values_list('idLogro', flat=True)
        return Logro.objects.exclude(idLogro__in=logrosObtenidos).order_by('idLogro')


class Mensaje(models.Model):
    idMensaje = models.AutoField(db_column='idMensaje', primary_key=True)  
    idEmisor = models.ForeignKey('Usuario', models.CASCADE, db_column='idEmisor')  
    fechaHora = models.DateTimeField(db_column='fechaHora') 
    texto = models.CharField(blank=True, null=True, max_length=200)
    idChat = models.ForeignKey(Chat, models.CASCADE, db_column='idChat')

    class Meta:
        managed = False
        db_table = 'mensaje'

    def __str__(self):
        return str(self.idMensaje) + ': ' + str(self.idEmisor.nombreUsuario) + ' a ' + str(self.fechaHora) + ' en ' + str(self.idChat)


class Notificacion(models.Model):
    idNotificacion = models.AutoField(db_column='idNotificacion', primary_key=True)
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario')
    texto = models.CharField(blank=True, null=True, max_length=100)
    fechaHora = models.DateTimeField(db_column='fechaHora')

    class Meta:
        managed = False
        db_table = 'notificacion'

    def __str__(self):
        return str(self.idNotificacion) + ': ' + str(self.idUsuario.nombreUsuario) + ' a ' + str(self.fechaHora)


class Prestamo(models.Model):
    idPrestamo = models.AutoField(db_column='idPrestamo', primary_key=True)
    fechaInicio = models.DateField(db_column='fechaInicio') 
    fechaFin = models.DateField(db_column='fechaFin')
    idProducto = models.ForeignKey('Producto', models.SET_NULL, null=True, db_column='idProducto')
    idArrendador = models.ForeignKey('Usuario', models.SET_NULL, null=True, db_column='idArrendador') 
    idArrendatario = models.ForeignKey('Usuario', models.SET_NULL, null=True, db_column='idArrendatario', related_name='prestamo_idarrendatario_set')
    condiciones = models.CharField(max_length=300)
    estado = models.CharField(blank=True, null=True, max_length=10, choices=(('Pendiente','Pendiente'), ('Aceptado', 'Aceptado'), ('Denegado', 'Denegado'), ('Finalizado', 'Finalizado')))

    class Meta:
        managed = False
        db_table = 'prestamo'

    def __str__(self):
        return str(self.idPrestamo) + ': ' + str(self.idArrendador.nombreUsuario) + ' a ' + str(self.idArrendatario.nombreUsuario) + ': ' + str(self.estado)
    
    def guardarPrestamo(self):
        self.save()
    
    @staticmethod
    def getPrestamoPorId(idPrestamo):
        try:
            return Prestamo.objects.get(idPrestamo = idPrestamo)
        except:
            return False

    @staticmethod
    def getPrestamosPorUsuario(idUsuario):
        try:
            prestamosArrendador =  Prestamo.objects.filter(idArrendador=idUsuario)
            try: 
                prestamosArrendatario = Prestamo.objects.filter(idArrendatario=idUsuario)
                return prestamosArrendador | prestamosArrendatario
            except:
                return prestamosArrendador
        except:
            return []
    @staticmethod    
    def getRegistroPrestamosPorUsuario(idUsuario):
        try:
            prestamosArrendador = Prestamo.objects.filter(idArrendador=idUsuario, estado__in=['Aceptado', 'Finalizado']).order_by('-idPrestamo')
            try: 
                prestamosArrendatario = Prestamo.objects.filter(idArrendatario=idUsuario, estado__in=['Aceptado', 'Finalizado']).order_by('-idPrestamo')
                return prestamosArrendador | prestamosArrendatario
            except:
                return prestamosArrendador
        except:
            return []
        
    @staticmethod    
    def getRegistroPrestamosPendientesPorUsuario(idUsuario):
        try:
            prestamosArrendador = Prestamo.objects.filter(idArrendador=idUsuario, estado__in=['Pendiente'])
            return prestamosArrendador
        except:
            return []
    

    @staticmethod
    def existePrestamoPendiente(idArrendatario, idProducto):
        try:
            return Prestamo.objects.get(idArrendatario = idArrendatario, idProducto = idProducto, estado__in=['Pendiente'])
        except:
            return False

    @staticmethod
    def existePrestamoAceptado(idArrendador, idProducto):
        try:
            return Prestamo.objects.get(idArrendador = idArrendador, idProducto = idProducto, estado__in=['Aceptado'])
        except:
            return False
        

class Producto(models.Model):
    idProducto = models.AutoField(db_column='idProducto', primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(blank=True, null=True, max_length=300)
    disponibilidad = models.IntegerField()
    idPropietario = models.ForeignKey('Usuario', models.CASCADE, db_column='idPropietario') 
    fechaSubida = models.DateTimeField(db_column='fechaSubida')
    fotoProducto = models.ForeignKey(PrivateAttachment, models.SET_NULL, db_column='fotoProducto', null=True, blank=True)
    

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return str(self.idProducto) + ': ' + self.nombre
    
    def guardarProducto(self):
        self.save()
    
    @staticmethod
    def getTodosProductos():
        return Producto.objects.all()

    @staticmethod
    def getTodosProductosOrden():
        
        return Producto.objects.all().order_by('-fechaSubida')
    
    @staticmethod
    def getProductosDeUsuario(nombreUsuario):
        return Producto.objects.filter(idPropietario = nombreUsuario)

    @staticmethod
    def getProductoPorId(idProducto):
        return Producto.objects.get(idProducto = idProducto)
    
    @staticmethod
    def getCategoriasDeProducto(idProducto):
        try:
            return CategoriaProducto.objects.filter(idProducto = idProducto)
        except:
            return False
    @staticmethod
    def getProductosPorTexto(texto):
        if not texto:
            return Producto.objects.all()
        
        return Producto.objects.filter(nombre__icontains=texto)

    @staticmethod
    def getProductosPorTextoOrden(texto):
        if not texto:
            return Producto.objects.all()
        
        return Producto.objects.filter(nombre__icontains=texto).order_by('-fechaSubida')

class CategoriaProducto(models.Model):
    idCategoriaProducto = models.AutoField(db_column='idCategoriaProducto', primary_key=True)
    idCategoria = models.ForeignKey(Categoria, models.CASCADE, db_column='idCategoria')
    idProducto = models.ForeignKey(Producto, models.CASCADE, db_column='idProducto')
    
    class Meta:
        managed = False
        db_table = 'categoriaproducto'

    def __str__(self):
        return str(self.idCategoria.nombre) + ' - ' + str(self.idProducto.nombre)
    
    def nuevaCategoriaProducto(self):
        self.save()
    
    @staticmethod
    def existeCategoriaProducto(idCategoria, idProducto):
        try:
            return CategoriaProducto.objects.get(idCategoria = idCategoria, idProducto = idProducto)
        except: 
            return False



class Usuario(models.Model):
    idUsuario = models.AutoField(db_column='idUsuario', primary_key=True) 
    nombre = models.CharField(blank=True, null=True, max_length=20)
    apellidos = models.CharField(blank=True, null=True, max_length=50)
    correo = models.EmailField(unique=True, max_length=80)
    contrasena = models.CharField(max_length=80)
    nombreUsuario = models.CharField(db_column='nombreUsuario', unique=True, max_length=20) 
    ubicacion = models.CharField(blank=True, null=True, max_length=20)
    fotoPerfil = models.ForeignKey(PrivateAttachment, models.SET_NULL, db_column='fotoPerfil', null=True, blank=True)
    # idProductosFavoritos = models.CharField(db_column='idProductosFavoritos', blank=True, null=True, max_length=30) 
    # idUsuariosFavoritos = models.CharField(db_column='idUsuariosFavoritos', blank=True, null=True, max_length=30) 
    rol = models.CharField(max_length=13, choices=(('administrador','administrador'), ('usuario', 'usuario')))

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.rol + ': ' + self.nombreUsuario
    
    def registro(self):
        self.save()


    @staticmethod
    def getUsuarioPorNombreUsuario(nombreUsuario):
        try:
            return Usuario.objects.get(nombreUsuario=nombreUsuario)
        except:
            return False
    
    @staticmethod
    def getUsuarioPorId(idUsuario):
        try:
            return Usuario.objects.get(idUsuario=idUsuario)
        except:
            return False


    def existe(self):
        if Usuario.objects.filter(nombreUsuario=self.nombreUsuario):
            return True
        return False
    
    
    @staticmethod
    def existeCorreo(correo):
        if Usuario.objects.filter(correo=correo):
            return True
        return False

class Reporte(models.Model):
    idReporte = models.AutoField(db_column='idReporte', primary_key=True) 
    idEmisor = models.ForeignKey(Usuario, models.CASCADE, db_column='idEmisor')  
    idReceptor = models.ForeignKey(Usuario, models.CASCADE, db_column='idReceptor', related_name='reporte_idreceptor_set')       
    idProducto = models.ForeignKey(Producto, models.CASCADE, db_column='idProducto', blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True, max_length=200)
    fechaHora = models.DateTimeField(db_column='fechaHora')

    class Meta:
        managed = False
        db_table = 'reporte'
    
    def __str__(self):
        return str(self.idReporte) + ': ' + str(self.idEmisor) + ': ' + str(self.descripcion)
    
    @staticmethod
    def getReporteProducto(idEmisor, idProducto):
        try:
            return Reporte.objects.get(idEmisor = idEmisor, idProducto = idProducto)
        except:
            return False
    
    @staticmethod
    def getReporteUsuario(idEmisor, idReceptor):
        try:
            return Reporte.objects.get(idEmisor=idEmisor, idReceptor=idReceptor, idProducto=None)
        except:
            return False

class Valoracion(models.Model):
    idValoracion = models.AutoField(db_column='idValoracion', primary_key=True) 
    idEmisor = models.ForeignKey(Usuario, models.CASCADE, db_column='idEmisor')  
    idReceptor = models.ForeignKey(Usuario, models.CASCADE, db_column='idReceptor', related_name='valoracion_idreceptor_set')       
    puntuacion = models.IntegerField()
    comentario = models.CharField(blank=True, null=True, max_length=300)
    idProducto = models.ForeignKey(Producto, models.CASCADE, db_column='idProducto', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valoracion'

    def __str__(self):
        return 'DE: ' + str(self.idEmisor.nombreUsuario) + ' A: ' + str(self.idReceptor.nombreUsuario)
    
    def guardarValoracion(self):
        self.save()

    @staticmethod
    def getValoracionesDeProducto(idProducto):
        try:
            return Valoracion.objects.filter(idProducto = idProducto )
        except:
            return False
    @staticmethod
    def getValoracionesPerfil(idUsuario):
        try:
            return Valoracion.objects.filter(idReceptor = idUsuario, idProducto__isnull=True)
        except:
            return False
        
    @staticmethod
    def getPuntuaciónProducto(idProducto):
        try:
            media = Valoracion.objects.filter(idProducto = idProducto).aggregate(media=Avg('puntuacion'))['media']
            return media
        except:
            return '-'
        
    @staticmethod
    def existeValoracionProducto(idEmisor,idProducto):
        if Valoracion.objects.filter(idEmisor = idEmisor, idProducto = idProducto):
            return True
        return False
    @staticmethod
    def getValoracionProducto(idEmisor, idProducto):
        if Valoracion.existeValoracionProducto(idEmisor, idProducto):
            return Valoracion.objects.get(idEmisor = idEmisor, idProducto = idProducto)
        return False
    
    @staticmethod
    def existeValoracionUsuario(idEmisor,idReceptor):
        if Valoracion.objects.filter(idEmisor = idEmisor, idReceptor = idReceptor, idProducto__isnull=True):
            return True
        return False
    @staticmethod
    def getValoracionUsuario(idEmisor, idReceptor):
        if Valoracion.existeValoracionUsuario(idEmisor, idReceptor):
            return Valoracion.objects.get(idEmisor = idEmisor, idReceptor = idReceptor, idProducto__isnull=True)
        return False
    