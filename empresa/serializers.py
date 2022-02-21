import datetime
from rest_framework import serializers
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
    fecha_actual = datetime.datetime.now().strftime('%d/%m/%Y')
    #fecha_fin = serializers.DateField(initial=fecha_actual)
    class Meta:
        model = Participa
        fields = ['idProyecto','fechaInscripcion','rol']
        depth = 1
        