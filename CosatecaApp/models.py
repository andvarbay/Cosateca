from django.db import models

# Create your models here.

class Usuario(models.Model):

    nombre = models.CharField(blank=True, null=True, max_length=20)
    apellidos = models.CharField(blank=True, null=True, max_length=50)
    correo = models.CharField(unique=True, max_length=80)
    contrasenha = models.CharField(max_length=80)
    nombreusuario = models.CharField(db_column='nombreUsuario', unique=True, max_length=20)  # Field name made lowercase.
    ubicacion = models.CharField(blank=True, null=True, max_length=20)
    rol = models.CharField(blank=True, null=True, max_length=13, choices=(('administrador','administrador'), ('usuario', 'usuario')))

    class Meta:
        managed = False
        db_table = 'usuario'