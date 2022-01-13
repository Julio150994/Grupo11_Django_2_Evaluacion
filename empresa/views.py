from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from empresa.models import Cliente, Usuario
from .forms import ClienteModelForm, UsuarioModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    
    if request.method == 'POST':
        usuario = UsuarioModelForm(request.POST)
        cliente = ClienteModelForm(request.POST)
        context = {
            'usuario': usuario,
            'cliente': cliente
        }
        
        if usuario.is_valid():
            # Añadimos datos de usuario #
            request.POST['username']
            request.POST['password']
            usuario.save()
            
            if cliente.is_valid():
               #try:
                # Consulta en SQL: SELECT id FROM usuario ORDER BY id DESC LIMIT 1 #
                last_id_usuario = Usuario.objects.last()
                dni = request.POST.get('dni')
                nombre = request.POST.get('nombre')
                apellidos = request.POST.get('apellidos')
                direccion = request.POST.get('direccion')
                fechaNacimiento = request.POST.get('fechaNacimiento')
                fechaAlta = request.POST.get('fechaAlta')
                activo = request.POST.get('activo',False)
                idUsuario = request.POST.get('idUsuario',last_id_usuario)
                
                if dni is not None or nombre is not None or apellidos is not None or direccion is not None or fechaNacimiento is not None or fechaAlta is not None or activo is not None or idUsuario:
                    # Añadimos datos de cliente #
                    """dni=request.POST.get['dni'], nombre=request.POST.get['nombre'],
                    apellidos=request.POST.get['apellidos'], direccion=request.POST.get['direccion'],
                    fechaNacimiento=request.POST.get['fechaNacimiento'], fechaAlta=request.POST.get['fechaAlta'],
                    activo=request.POST.get('activo',False), idUsuario=request.POST.get('idUsuario',str(last_id_usuario))"""
                
                    #nuevo_cliente = Cliente(Cliente.objects.get('id'),dni,nombre,apellidos,direccion,fechaNacimiento,fechaAlta,activo,idUsuario)
                    nuevo_cliente = Cliente.objects.all()
                    cliente.save(nuevo_cliente)
                    messages.success(request,'Cliente registrado correctamente.')
                else:
                    messages.warning(request,'Faltan datos por introducir.')
                    return redirect('registro_cliente')
                return redirect('users_login')
            """except Exception as ex:
                messages.error(request,'Error al registrar cliente.')
                return redirect('registro_cliente')"""
               
    return render(request, "empresa/registro_cliente.html",context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']

        user = authenticate(username=username, password=pwd)
        #name = user.nombre
        # {'name': name} #
        if user is not None:
            login(request, user)
            messages.success(request,str(username)+' ha iniciado sesión correctamente.')
            #return render(request,"empresa/page_inicio.html")
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
    #perfil_cliente = Cliente.objects.get(id = id)

    if request.method == 'GET':
        usuario = UsuarioModelForm(instance = datos_usuario)
        #cliente = ClienteModelForm(instance = perfil_cliente)
        context = {
            'usuario':usuario
            #'cliente':cliente
        }
    else:
        usuario = UsuarioModelForm(request.POST, instance = datos_usuario)
        #cliente = ClienteModelForm(request.POST, instance = perfil_cliente)
        context = {
            'usuario':usuario,
            #'cliente':cliente
        }
        
        if usuario.is_valid():
            usuario.save()
        
            """if cliente.is_valid():
                cliente.save()
                return redirect('page_inicio')"""
        
    return render(request,'empresa/perfil_cliente.html',context) 