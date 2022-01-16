from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.id)+" "+str(self.username)+" "+str(self.password)
    

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=9,unique=True)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150)
    biografia = models.CharField(max_length=255)
    idUsuario = models.ForeignKey(Usuario, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)+" "+str(self.dni)+" "+str(self.nombre)+" "+str(self.apellidos)+" "+str(self.direccion)+" "+str(self.biografia)
    
    
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=9,unique=True)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150)
    fechaNacimiento = models.DateField(auto_now=False)
    fechaAlta = models.DateField(auto_now=False)
    activo = models.BooleanField(default=False)
    idUsuario = models.ForeignKey(Usuario, blank=False, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.id)+" "+str(self.dni)+" "+str(self.nombre)+" "+str(self.apellidos)+" "+str(self.direccion)+" "+str(self.fechaNacimiento)+" "+str(self.fechaAlta)

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    foto = models.ImageField(verbose_name="Foto", upload_to='imagenes', null=False)
    
    def __str__(self):
        return str(self.id)+" "+str(self.nombre)+" "+str(self.foto)
    
    
class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=255)
    nivel = models.IntegerField()
    fechaInicio = models.DateField(auto_now=True)
    fechaFin = models.DateField(auto_now=True)
    informeFinal = models.CharField(max_length=255)
    idEmpleado = models.ForeignKey(Empleado, on_delete = models.CASCADE)
    idCategoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.id)+" "+str(self.titulo)+" "+str(self.descripcion)+" "+str(self.nivel)+" "+str(self.fechaInicio)+" "+str(self.fechaFin)+" "+str(self.informeFinal)+" "+str(self.idEmpleado)+" "+str(self.idCategoria)
    
    
class Participa(models.Model):
    id = models.AutoField(primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    idProyecto = models.ForeignKey(Proyecto, on_delete = models.CASCADE)
    fechaInscripcion = models.DateField(auto_now=True)
    rol = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.id)+" "+str(self.idCliente)+" "+str(self.idProyecto)+" "+str(self.fechaInscripcion)+" "+str(self.rol)