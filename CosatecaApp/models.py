from django.db import models

# Create your models here.

class Categoria(models.Model):
    idCategoria = models.AutoField(db_column='idCategoria', primary_key=True)  
    nombre = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'categoria'

    def __str__(self):
        return self.nombre


class Chat(models.Model):
    idChat = models.AutoField(db_column='idChat', primary_key=True) 
    idUsuarioArrendador = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuarioArrendador')  
    idUsuarioArrendatario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuarioArrendatario', related_name='chat_idusuarioarrendatario_set')  # Field name made lowercase.
    idProducto = models.ForeignKey('Producto', models.CASCADE, db_column='idProducto')  

    class Meta:
        managed = False
        db_table = 'chat'
    
    def __str__(self):
        return 'Chat ' + str(self.idChat)


class Estadistica(models.Model):
    idEstadistica = models.AutoField(db_column='idEstadistica', primary_key=True) 
    nombre = models.CharField(blank=True, null=True, max_length=40)
    descripcion = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'estadistica'
    
    def __str__(self):
        return self.nombre


class EstadisticaUsuario(models.Model):
    idEstadisticaUsuario = models.AutoField(db_column='idEstadisticaUsuario', primary_key=True)  
    idEstadistica = models.ForeignKey(Estadistica, models.CASCADE, db_column='idEstadistica')  
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario') 
    valor = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estadisticausuario'

    def __str__(self):
        return str(self.idEstadisticaUsuario) + ': ' + str(self.idEstadistica) + ' - ' + str(self.idUsuario)


class Listado(models.Model):
    idListado = models.AutoField(db_column='idListado', primary_key=True)  
    nombre = models.CharField(max_length=20)
    productos = models.CharField(blank=True, null=True, max_length=20)
    idPropietario = models.ForeignKey('Usuario', models.CASCADE, db_column='idPropietario') 

    class Meta:
        managed = False
        db_table = 'listado'

    def __str__(self):
        return self.nombre + ' de ' + str(self.idPropietario)


class Logro(models.Model):
    idLogro = models.AutoField(db_column='idLogro', primary_key=True) 
    nombre = models.CharField(blank=True, null=True, max_length=40)
    descripcion = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'logro'

    def __str__(self):
        return self.nombre


class LogroUsuario(models.Model):
    idLogroUsuario = models.AutoField(db_column='idLogroUsuario', primary_key=True) 
    idLogro = models.ForeignKey('Logro', models.CASCADE, db_column='idLogro')  
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario') 
    fechaObtencion = models.DateField(db_column='fechaObtencion') 

    class Meta:
        managed = False
        db_table = 'logrousuario'

    def __str__(self):
        return str(self.idLogroUsuario) + ': ' + str(self.idLogro) + ' - ' + str(self.idUsuario)


class Mensaje(models.Model):
    idMensaje = models.AutoField(db_column='idMensaje', primary_key=True)  
    idEmisor = models.IntegerField(db_column='idEmisor')  
    fechaHora = models.DateTimeField(db_column='fechaHora') 
    texto = models.CharField(blank=True, null=True, max_length=200)
    idChat = models.ForeignKey(Chat, models.CASCADE, db_column='idChat')

    class Meta:
        managed = False
        db_table = 'mensaje'

    def __str__(self):
        return str(self.idMensaje) + ': ' + str(self.idEmisor) + ' a ' + str(self.fechaHora)


class Notificacion(models.Model):
    idNotificacion = models.AutoField(db_column='idNotificacion', primary_key=True)
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario')
    texto = models.CharField(blank=True, null=True, max_length=100)
    fechaHora = models.DateTimeField(db_column='fechaHora')

    class Meta:
        managed = False
        db_table = 'notificacion'

    def __str__(self):
        return str(self.idNotificacion) + ': ' + str(self.idUsuario) + ' a ' + str(self.fechaHora)


class Prestamo(models.Model):
    idPrestamo = models.AutoField(db_column='idPrestamo', primary_key=True)
    fechaInicio = models.DateField(db_column='fechaInicio') 
    fechaFin = models.DateField(db_column='fechaFin')
    idProducto = models.ForeignKey('Producto', models.CASCADE, db_column='idProducto')
    idArrendador = models.ForeignKey('Usuario', models.CASCADE, db_column='idArrendador') 
    idArrendatario = models.ForeignKey('Usuario', models.CASCADE, db_column='idArrendatario', related_name='prestamo_idarrendatario_set')
    condiciones = models.CharField(max_length=300)
    estado = models.CharField(blank=True, null=True, max_length=10, choices=(('Pendiente','Pendiente'), ('Aceptado', 'Aceptado'), ('Denegado', 'Denegado'), ('Finalizado', 'Finalizado')))

    class Meta:
        managed = False
        db_table = 'prestamo'

    def __str__(self):
        return str(self.idPrestamo) + ': ' + self.estado


class Producto(models.Model):
    idProducto = models.AutoField(db_column='idProducto', primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(blank=True, null=True, max_length=300)
    disponibilidad = models.IntegerField()
    idPropietario = models.ForeignKey('Usuario', models.CASCADE, db_column='idPropietario') 
    # idCategorias = models.CharField(db_column='idCategorias', blank=True, null=True, max_length=20) 
    # idCategorias = models.ManyToManyField(Categoria)
    fechaSubida = models.DateTimeField(db_column='fechaSubida')

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return str(self.idProducto) + ': ' + self.nombre
    
    @staticmethod
    def getTodosProductos():
        return Producto.objects.all()

class CategoriaProducto(models.Model):
    idCategoriaProducto = models.AutoField(db_column='idCategoriaProducto', primary_key=True)
    idCategoria = models.ForeignKey(Categoria, models.CASCADE, db_column='idCategoria')
    idProducto = models.ForeignKey(Producto, models.CASCADE, db_column='idProducto')
    
    class Meta:
        managed = False
        db_table = 'categoriaproducto'

    def __str__(self):
        return 'cat: '+ str(self.idCategoria.nombre) + ' prod: ' + str(self.idProducto.nombre)


class Reporte(models.Model):
    idReporte = models.AutoField(db_column='idReporte', primary_key=True) 
    idUsuario = models.ForeignKey('Usuario', models.CASCADE, db_column='idUsuario')
    idProducto = models.ForeignKey(Producto, models.CASCADE, db_column='idProducto', blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True, max_length=200)
    fechaHora = models.DateTimeField(db_column='fechaHora')

    class Meta:
        managed = False
        db_table = 'reporte'
    
    def __str__(self):
        return str(self.idReporte) + ': ' + str(self.idUsuario) + ' a ' + str(self.fechaHora)

class Usuario(models.Model):
    idUsuario = models.AutoField(db_column='idUsuario', primary_key=True) 
    nombre = models.CharField(blank=True, null=True, max_length=20)
    apellidos = models.CharField(blank=True, null=True, max_length=50)
    correo = models.CharField(unique=True, max_length=80)
    contrasena = models.CharField(max_length=80)
    nombreUsuario = models.CharField(db_column='nombreUsuario', unique=True, max_length=20) 
    ubicacion = models.CharField(blank=True, null=True, max_length=20)
    # idProductosFavoritos = models.CharField(db_column='idProductosFavoritos', blank=True, null=True, max_length=30) 
    # idUsuariosFavoritos = models.CharField(db_column='idUsuariosFavoritos', blank=True, null=True, max_length=30) 
    rol = models.CharField(blank=True, null=True, max_length=13, choices=(('administrador','administrador'), ('usuario', 'usuario')))

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nombreUsuario + ' ' + self.rol


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
        return 'De: ' + str(self.idEmisor) + ' para ' + str(self.idReceptor)