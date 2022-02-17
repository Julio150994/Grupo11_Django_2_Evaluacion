import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Cliente, Empleado, Participa, Proyecto, Usuario
from .forms import CategoriaModelForm, ClienteSerializers, EmpleadoModelForm, FinProyectoModelForm, ProyectoModelForm, UsuarioModelForm, UsuarioSerializers
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


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
        
class ClienteUsuarioAPI(APIView):
    def get(self, request, format=None, *args, **kwargs):
        #cliente = Cliente.objects.order_by('-id').all()
        #usuario = Usuario.objects.get()
        
        serial_cliente = [[cliente.dni, cliente.nombre, cliente.apellidos, cliente.direccion, cliente.fechaNacimiento.strftime('%d/%m/%Y'),
                           cliente.fechaAlta.strftime('%d/%m/%Y'), cliente.idUsuario.username] for cliente in Cliente.objects.order_by('-id')]
        
        #serial_cliente = ClienteSerializers(cliente, many=True)
        #serial_usuario = UsuarioSerializers(usuario, many=True)
        return Response(serial_cliente)
    

class ProyectosClienteAPI(APIView):
    def get(self, request, format=None, *args, **kwargs):
        fecha_actual = datetime.datetime.now().strftime('%d/%m/%Y')
        
        serial_proyectos_cli = [[participa.idCliente.idUsuario.username, participa.idProyecto.titulo, participa.idProyecto.descripcion,
                                participa.idProyecto.nivel, participa.idProyecto.fechaInicio.strftime('%d/%m/%Y'), participa.idProyecto.fechaFin.strftime('%d/%m/%Y'),
                                participa.idProyecto.informeFinal, participa.fechaInscripcion.strftime('%d/%m/%Y'), participa.rol]
                                for participa in Participa.objects.order_by('-id')
                                if participa.idCliente.idUsuario.username == request.user.username and participa.idProyecto.fechaFin.strftime('%d/%m/%Y') < fecha_actual]
        
        #serial_participa = ProyectosClienteSer(participa_pry, many=True)
        return Response(serial_proyectos_cli)