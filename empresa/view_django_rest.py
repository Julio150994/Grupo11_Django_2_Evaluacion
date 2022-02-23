from lib2to3.pgen2.parse import ParseError
from empresa.models import Cliente, Empleado, Participa, Usuario
from .serializers import ParticipaSerializer
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class TokenView(APIView):
    def get(self, request, format=None):
        return Response({'detail':"Respuesta GET"})
    
    def post(self, request, format=None, *args, **kwargs):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Formato JSON inválido - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if "user" not in data or "password" not in data:
            return Response(
                'Error al introducir las credenciales',
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = User.objects.get(username=data["user"])

        if not user:
            return Response(
                'Cliente no encontrado en la base de datos.',
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            if user.is_active:
                token, get_token = Token.objects.get_or_create(user=user)
                
                if get_token:
                    # Generamos y/o eliminamos token para generar otro nuevo #
                    return Response({
                        'detail': 'Ha iniciado sesión correctamente',
                        'token': token.key
                    }, status = status.HTTP_201_CREATED)
  
                else:
                    token.delete()
                    Response({
                        'error': 'Ya se ha iniciado sesión con este cliente',
                    }, status = status.HTTP_409_CONFLICT)
                    
                return redirect('api_token')
                
            else:
                return Response({
                    'detail': 'Error. El usuario debe ser un cliente'
                }, status= status.HTTP_401_UNAUTHORIZED)
    
    
class ProyectosClienteAPIView(APIView):
    permission_class = [IsAuthenticated]
    
    def get(self, request, format=None, *args, **kwargs):
        participa = Participa.objects.order_by('-id')
        
        serial_proyectos_cli = ParticipaSerializer(participa, many=True)
        return Response(serial_proyectos_cli.data)