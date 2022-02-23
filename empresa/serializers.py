import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from empresa.models import Cliente, Participa, Usuario

"""Para realizar serializaciones con api rest en django"""
# Iniciamos sesión con usuarios que sean clientes #
class UsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','password']

class ClienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['idCliente']
        depth = 1


# Mostrar los proyectos en los que participa el cliente #
class ParticipaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Participa
        fields = ['idCliente','idProyecto','fechaInscripcion','rol']  
    
    def to_representation(self, instance):
        fecha_actual = datetime.date(int(datetime.date.today().year), int(datetime.date.today().month), int(datetime.date.today().day))
        fecha_fin = datetime.date(int(instance.idProyecto.fechaFin.year),int(instance.idProyecto.fechaFin.month), int(instance.idProyecto.fechaFin.day))

        if fecha_fin < fecha_actual and instance.idCliente.idUsuario.username == "frango1994":
            return  {
                'titulo':instance.idProyecto.titulo,
                'descripcion':instance.idProyecto.descripcion,
                'nivel':instance.idProyecto.nivel,
                'fechaInicio':instance.idProyecto.fechaInicio.strftime('%d/%m/%Y'),
                'fechaFin':instance.idProyecto.fechaFin.strftime('%d/%m/%Y'),
                'informeFinal':instance.idProyecto.informeFinal,
                'fechaInscripcion':instance.fechaInscripcion.strftime('%d/%m/%Y'),
                'rol':instance.rol,
            }