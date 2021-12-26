from django.db import models

# Create your models here.

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.id+" "+self.username+" "+self.password
    

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=9)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150)
    biografia = models.CharField(max_length=255)
    idUsuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.id+" "+self.dni+" "+self.nombre+" "+self.apellidos+" "+self.direccion+" "+self.biografia+" "+self.idUsuario
    
    
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=9)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150)
    fechaNacimiento = models.DateField(auto_now=True)
    fechaAlta = models.DateField(auto_now=True)
    activo = models.BooleanField()
    idUsuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.id+" "+self.dni+" "+self.nombre+" "+self.apellidos+" "+self.direccion+" "+self.fechaNacimiento+" "+self.fechaAlta+" "+self.activo+" "+self.idUsuario


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    foto = models.ImageField(verbose_name="Foto", upload_to='imagenes', null=False)
    
    def __str__(self):
        return self.id+" "+self.nombre+" "+self.foto
    
    
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
        return self.id+" "+self.titulo+" "+self.descripcion+" "+self.nivel+" "+self.fechaInicio+" "+self.fechaFin+" "+self.informeFinal+" "+self.idEmpleado+" "+self.idCategoria
    
    
class Participa(models.Model):
    id = models.AutoField(primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    idProyecto = models.ForeignKey(Proyecto, on_delete = models.CASCADE)
    fechaDescripcion = models.DateField(auto_now=True)
    rol = models.CharField(max_length=100)
    
    def __str__(self):
        return self.id+" "+self.idCliente+" "+self.idProyecto+" "+self.fechaDescripcion+" "+self.rol