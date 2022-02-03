from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from empresa.forms import ClienteModelForm
from empresa.models import Cliente, Usuario
from .forms import ClienteModelForm, UsuarioModelForm


def mostrar_clientes(request):
    listClientes = Cliente.objects.order_by('-id').all()
    context = { 'clientes': listClientes }
    return render(request,'empresa/clientes.html',context)


def datos_cliente(request,id):
    cliente = Cliente.objects.get(id = id)
    context = {'cliente':cliente}
    return render(request,'empresa/datos_cliente.html',context)


def get_actived(request,id):
    cliente = Cliente.objects.get(id = id)
    print("Cliente: "+str(cliente))
    
    print("Activo: "+str(cliente.activo))
    
    if cliente.activo == False:
        cliente.activo = True
        cliente.save()
        messages.success(request,"Cliente activado corretamente")
    else:
        cliente.activo = False
        cliente.save()
        messages.success(request,"Cliente desactivado corretamente")
    
    return redirect('clientes')


def annadir_clientes(request):
    usuario = UsuarioModelForm()
    cliente = ClienteModelForm()
    context = {
        'usuario':usuario,
        'cliente':cliente
    }

    if request.POST:
        usuario = UsuarioModelForm(request.POST)
        cliente = ClienteModelForm(request.POST)
        context = {
            'usuario':usuario,
            'cliente':cliente
        }
        
        if usuario.is_valid():
            username = request.POST['username']
            pwd = request.POST['password']
            
            nuevo_usuario = Usuario(username=username, password=pwd)
            nuevo_usuario.password = make_password(nuevo_usuario.password)
            nuevo_usuario.save()
            user = User.objects.create_user(username = username, password = pwd)
            user.save()

            if cliente.is_valid():
                last_id_usuario = Usuario.objects.last() 
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellidos = request.POST.get("apellidos")
                direccion = request.POST.get("direccion")
                fechaNacimiento = request.POST.get("fechaNacimiento")
                fechaAlta = request.POST.get("fechaAlta")
                activo = request.POST.get("activo",'') == 'off'
                idUsuario = request.POST.get("idUsuario",last_id_usuario)

                if dni is not None or nombre is not None or apellidos is not None or direccion is not None or fechaNacimiento is not None or fechaAlta is not None or activo is not None or idUsuario:
                    nuevo_cliente = Cliente(dni=dni, nombre=nombre, apellidos=apellidos, direccion=direccion,
                        fechaNacimiento=fechaNacimiento, fechaAlta=fechaAlta,activo=activo,idUsuario=idUsuario)
                    nuevo_cliente.save()
                    messages.success(request,'Cliente registrado correctamente.')
                    return redirect('clientes')
            else:
                messages.warning(request,'Faltan datos de cliente por introducir.')
                return redirect('form_add_cliente')
        else:
            messages.warning(request,'Faltan datos de usuario por introducir.')
            return redirect('form_add_cliente')

    return render(request, "empresa/form_add_cliente.html",context)


def editar_clientes(request,id):
    id_cliente = Cliente.objects.get(id = id)
    context = {'cliente':id_cliente}
    
    if request.method == 'POST':
        cliente = ClienteModelForm(request.POST, instance=id_cliente)
        context = {'cliente': cliente}
        
        if cliente.is_valid(): 
            dni = request.POST.get("dni")
            nombre = request.POST.get("nombre")
            apellidos = request.POST.get("apellidos")
            direccion = request.POST.get("direccion")
            fechaNacimiento = request.POST.get("fechaNacimiento")
            fechaAlta = request.POST.get("fechaAlta")
            activo = request.POST.get("activo",'') == 'off'
            idUsuario = request.POST.get("idUsuario")
            username = request.POST.get("username")
            password = request.POST.get("password")

            if dni is not None or nombre is not None or apellidos is not None or direccion is not None or fechaNacimiento is not None or fechaAlta is not None or activo is not None or idUsuario is not None:
                cliente.save()
                messages.success(request,'Cliente editado correctamente.')
                return redirect('clientes')
        else:
            messages.warning(request,'Faltan datos de usuario por introducir.')
            return redirect('clientes')
    
    return render(request, "empresa/form_edit_cliente.html",context)

def eliminar_cliente(request,id):
    cliente = Cliente.objects.filter(id=id)
    print(cliente)
    

    cliente.delete()
    
    messages.error(request,'Cliente eliminado éxitosamente.')
    return redirect('clientes')