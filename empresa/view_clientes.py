from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from empresa.forms import ClienteModelForm
from empresa.models import Cliente, Usuario
from .forms import ClienteModelForm


def mostrar_clientes(request):
    listClientes = Cliente.objects.all()
    context = { 'clientes': listClientes }
    return render(request,'empresa/clientes.html',context)

def annadir_clientes(request):
    cliente = ClienteModelForm()
    context = {'cliente':cliente}

    if request.POST:
        cliente = ClienteModelForm(request.POST)
        context = {'cliente': cliente}
        
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
                # print("aqui 1")
                nuevo_cliente.save()
                messages.success(request,'Cliente registrado correctamente.')
                return redirect('clientes')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            print(cliente.errors)
            return redirect('form_add_cliente')

    return render(request, "empresa/form_add_cliente.html",context)

def editar_clientes(request,id):
    id_cliente = Cliente.objects.get(id = id)
    
    if request.method == 'GET':
        cliente = ClienteModelForm(instance = id_cliente)
        context = {'cliente': cliente}
    else:
        cliente = ClienteModelForm(request.POST, instance = id_cliente)
        context = {'cliente': cliente}
            
        if cliente.is_valid():
            cliente.save()
            #messages.success(request,'Categoría editada correctamente.')
            return reverse(redirect('clientes')+"?cliente_updated")
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_edit_cliente')
    
    return render(request, "empresa/form_edit_cliente.html",context)

def eliminar_cliente(request,id):
    cliente = Cliente.objects.get(id = id)
    context = {'cliente':cliente}
    
    if cliente is None:
        messages.warning(request,'No se ha podido eliminar este cliente.')
    else:
        cliente.delete()
        messages.error(request,'Cliente '+str(cliente)+' eliminado éxitosamente.')
    
    return render(request,'empresa/clientes.html',context)