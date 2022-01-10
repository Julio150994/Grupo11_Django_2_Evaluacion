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
                # Consulta en SQL: SELECT id FROM usuario ORDER BY id DESC LIMIT 1 #
                last_id_usuario = Usuario.objects.last()
                #id_usuario = Usuario.objects.filter(id=int(last_id_usuario[0:2])).values_list('id')
                #print("Id de usuario: "+str(last_id_usuario))
                #print(Usuario.objects.filter(id=int(last_id_usuario)).query())
                
                # Añadimos datos de cliente #
                request.POST['dni']
                request.POST['nombre']
                request.POST['apellidos']
                request.POST['direccion']
                request.POST['fechaNacimiento']
                request.POST['fechaAlta']
                request.POST[str(0)]
                request.POST[str(last_id_usuario)]
                
                cliente.save()
                #return redirect('sign_in')
                return redirect(reverse('sign_in'+"?registrado"))
        
    return render(request, "empresa/registro_cliente.html",context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']

        user = authenticate(username=username, password=pwd)

        if user is not None:
            login(request, user)
            #name = user.nombre
            # {'name': name} #
            return render(request,"empresa/page_inicio.html")
        
        else:
            messages.error(request, "Faltan credenciales por poner.")
            return redirect('page_inicio')

    return render(request, "empresa/sign_in.html")

def sign_out(request):
    logout(request)
    usuario = UsuarioModelForm()
    context = { 'usuario': usuario }
    
    return render(request,'empresa/sign_in.html',context)
