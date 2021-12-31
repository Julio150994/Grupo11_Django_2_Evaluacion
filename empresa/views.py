from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from empresa.models import Cliente, Usuario
from .forms import ClienteModelForm, UsuarioModelForm

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
    
    if request.method == "POST":
        usuario = UsuarioModelForm(request.POST)
        cliente = ClienteModelForm(request.POST)
        context = {
            'usuario': usuario,
            'cliente': cliente
        }
        
        if usuario.is_valid():
            usuario.save()
            #usuario_cliente = Usuario.objects.last()
            usuario_cliente = Usuario.objects.raw('SELECT id from Usuario ORDER BY DESC LIMIT 1')
            
            if cliente.is_valid():
                print("Id usuario: "+str(usuario_cliente))
                
                dni = request.POST.get('dni','')
                nombre = request.POST.get('nombre','')
                apellidos = request.POST.get('apellidos','')
                direccion = request.POST.get('direccion','')
                fechaNacimiento = request.POST.get('fechaNacimiento','')
                fechaAlta = request.POST.get('fechaAlta','')
                activo = request.POST.get('activo',0)
                idUsuario = request.GET.get('idUsuario',usuario_cliente)
                
                cliente.save()
                return redirect('login')
                #return redirect(reverse('login'+"?registrado"))
        
    return render(request, "empresa/registro_cliente.html",context)