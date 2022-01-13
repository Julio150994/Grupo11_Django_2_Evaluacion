from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from empresa.models import Cliente, Usuario
from .forms import ClienteModelForm, UsuarioModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your views here.

#---------Enlace a la plantilla escogida para el proyecto--------#
class InicioEmpresaView(TemplateView):
    template_name = "empresa/page_inicio.html"
    
def registrar_cliente(request):
    usuario = UsuarioModelForm()
    cliente = ClienteModelForm()
    context = {
        'usuario': usuario,
        'cliente': cliente
    }
    
    if request.POST:
        usuario = UsuarioModelForm(request.POST)
        cliente = ClienteModelForm(request.POST)
        context = {
            'usuario': usuario,
            'cliente': cliente
        }
        
        if usuario.is_valid():
            username = request.POST['username']
            pwd = request.POST['password']
            
            nuevo_usuario = Usuario(username=username, password=pwd)
            nuevo_usuario.password = make_password(nuevo_usuario.password)
            #user = User.objects.create(username = username, password=pwd)
            #user.save()
            nuevo_usuario.save()
            
            if cliente.is_valid():
                last_id_usuario = Usuario.objects.last()
                
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellidos = request.POST.get("apellidos")
                direccion = request.POST.get("direccion")
                fechaNacimiento = request.POST.get("fechaNacimiento")
                fechaAlta = request.POST.get("fechaAlta")
                activo = request.POST.get("activo",False)
                idUsuario = request.POST.get("idUsuario",last_id_usuario)
                
                if dni is not None or nombre is not None or apellidos is not None or direccion is not None or fechaNacimiento is not None or fechaAlta is not None or activo is not None or idUsuario:
                    nuevo_cliente = Cliente(dni=dni, nombre=nombre, apellidos=apellidos, direccion=direccion,
                        fechaNacimiento=fechaNacimiento, fechaAlta=fechaAlta,activo=activo,idUsuario=idUsuario)
                    nuevo_cliente.save()
                    messages.success(request,'Cliente registrado correctamente.')
                    return redirect('users_login')
                else:
                    messages.warning(request,'Faltan datos por introducir.')
                    return redirect('registro_cliente')
                
    return render(request, "empresa/registro_cliente.html",context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']

        user = authenticate(username=username, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request,str(username)+' ha iniciado sesión correctamente.')
            return redirect('page_inicio')
        else:
            messages.error(request,'Faltan credenciales por poner.')
            return redirect('users_login')

    return render(request, "empresa/sign_in.html")


def sign_out(request):
    logout(request)
    messages.success(request,' Ha cerrado sesión correctamente.')
    return redirect('users_login')


def vista_perfil(request, id):
    # Después de haber accedido con del rol de cliente #
    datos_usuario = Usuario.objects.get(id = id)
    perfil_cliente = Cliente.objects.get(id = id)

    if request.method == 'GET':
        usuario = UsuarioModelForm(instance = datos_usuario)
        cliente = ClienteModelForm(instance = perfil_cliente)
        context = {
            'usuario':usuario,
            'cliente':cliente
        }
    else:
        usuario = UsuarioModelForm(request.POST, instance = datos_usuario)
        cliente = ClienteModelForm(request.POST, instance = perfil_cliente)
        context = {
            'usuario':usuario,
            'cliente':cliente
        }
        
        if usuario.is_valid():
            username = request.POST['username']
            pwd = request.POST['password']
            
            perfil = Usuario(username=username, password=pwd)
            perfil.password = make_password(perfil.password)
            #user = User.objects.create_user(username = username, password=pwd)
            #user.save()
            perfil.save()
        
            if cliente.is_valid():
                last_id_usuario = Usuario.objects.last()
                
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellidos = request.POST.get("apellidos")
                direccion = request.POST.get("direccion")
                fechaNacimiento = request.POST.get("fechaNacimiento")
                fechaAlta = request.POST.get("fechaAlta")
                activo = request.POST.get("activo",False)
                idUsuario = request.POST.get("idUsuario",last_id_usuario)
                
                if dni is not None or nombre is not None or apellidos is not None or direccion is not None or fechaNacimiento is not None or fechaAlta is not None or activo is not None or idUsuario:
                    nuevo_cliente = Cliente(dni=dni, nombre=nombre, apellidos=apellidos, direccion=direccion,
                        fechaNacimiento=fechaNacimiento, fechaAlta=fechaAlta,activo=activo,idUsuario=idUsuario)
                    nuevo_cliente.save()
                    messages.success(request,'Perfil de cliente editado correctamente.')
                    return redirect('page_inicio')
                else:
                    messages.warning(request,'Faltan datos por introducir.')
                    return redirect('registro_cliente')
        
    return render(request,'empresa/perfil_cliente.html',context) 