from rest_framework import serializers
from empresa.models import Cliente, Participa, Proyecto, Usuario

"""Para realizar serializaciones con api rest en django"""
# Iniciamos sesión con cualquier usuario #
class UsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username','password']


# Mostrar los proyectos en los que participa el cliente #
class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['titulo','descripcion','nivel','fechaInicio','fechaFin','informeFinal']

class ParticipaSerializer(serializers.ModelSerializer):
    proyectos = ProyectoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Participa
        fields = ['proyectos','fechaInscripcion','rol']