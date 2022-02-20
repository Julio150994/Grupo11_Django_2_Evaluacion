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
    proyectos = ProyectoSerializer(many=True, read_only=True) #read_only=True#
    #proyectos = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Participa
        fields = ['proyectos','fechaInscripcion','rol']
        
    def create(self, validated_data):
        proyectos_data = validated_data.pop('proyectos')
        proyecto = Proyecto.objects.create(**validated_data)
        for proyecto_data in proyectos_data:
            Proyecto.objects.create(proyecto=proyecto, **proyecto_data)
        return proyecto