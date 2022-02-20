import datetime
from empresa.models import Categoria, Cliente, Empleado, Participa, Proyecto, Usuario
from .serializers import ParticipaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


"""class LoginUsuarioAPI(APIView):
    def get(self, request, format=None, *args, **kwargs):
        usuario = Usuario.objects.all()
        serial = UsuarioSerializers(usuario, many=True)
        return Response(serial.data)
    
    def post(self, request, format=None):
        serial = UsuarioSerializers(data=request.data)
        
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)"""
    

class ProyectosClienteAPI(APIView):
    def get(self, request, format=None, *args, **kwargs):
        fecha_actual = datetime.datetime.now().strftime('%d/%m/%Y')
        
        participa = Participa.objects.order_by('-id')
        #proyecto = Proyecto.objects.order_by('-id')
        
        serial_proyectos_cli = ParticipaSerializer(participa, many=True) #participa, many=True#
        return Response(serial_proyectos_cli.data)