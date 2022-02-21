from lib2to3.pgen2.parse import ParseError
from empresa.models import Cliente, Participa, Usuario
from .serializers import ParticipaSerializer, UsuarioSerializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class TokenView(APIView):
    def get(self, request, format=None):
        return Response({'detail':"Respuesta GET"})
    
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Formato JSON inválido - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if "username" not in data or "password" not in data:
            return Response(
                'Error en las credenciales',
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        cliente = Cliente.objects.get(username=data['cliente'])
        if not cliente:
             return Response(
                'Cliente no encontrado en la base de datos.',
                status=status.HTTP_404_NOT_FOUND
            )
        
        token = Token.objects.get_or_create(cliente=cliente)
        return Response({'detail': 'Respuesta POST', 'token':token[0].key})
    
class LoginClienteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, *args, **kwargs):
        usuario = Usuario.objects.all()
        cliente = Cliente.objects.all()
        
        serial = UsuarioSerializers(usuario, many=True)
        return Response(serial.data)
    
    def post(self, request, format=None):
        serializer_cliente = UsuarioSerializers(data=request.data)
        
        if serializer_cliente.is_valid():
            serializer_cliente.save()
            return Response(serializer_cliente.data, status=status.HTTP_201_CREATED)
        return Response(serializer_cliente.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProyectosClienteAPIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        participa = Participa.objects.order_by('-id')
        
        serial_proyectos_cli = ParticipaSerializer(participa, many=True)
        return Response(serial_proyectos_cli.data)