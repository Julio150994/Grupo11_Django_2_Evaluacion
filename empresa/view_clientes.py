from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from empresa.forms import ClienteModelForm
from empresa.models import Cliente
from .forms import ClienteModelForm


def mostrar_clientes(request):
    listClientes = Cliente.objects.all()
    context = { 'clientes': listClientes }
    return render(request,'empresa/clientes.html',context)

def annadir_clientes(request):
    cliente = ClienteModelForm()
    context = {'cliente':cliente}

    if request.method == 'POST':
        cliente = ClienteModelForm(request.POST, request.FILES)
        context = {'cliente': cliente}
        
        if cliente.is_valid():
            obj_cliente = Cliente.objects.get(pk=id)
            obj_cliente.titulo = cliente.cleaned_data['titulo']
            print("titulo: "+str(obj_cliente.titulo))
            obj_cliente.descripcion = cliente.cleaned_data['descripcion']
            print("descripcion: "+str(obj_cliente.descripcion))
            obj_cliente.nivel = cliente.cleaned_data['nivel']
            print("nivel: "+str(obj_cliente.nivel))
            obj_cliente.fechaInicio = cliente.cleaned_data['fechaInicio']
            print("fechaInicio: "+str(obj_cliente.fechaInicio))
            obj_cliente.fechaFin = cliente.cleaned_data['fechaFin']
            print("fechaFin: "+str(obj_cliente.fechaFin))
            obj_cliente.informeFinal = cliente.cleaned_data['informeFinal']
            print("informeFinal: "+str(obj_cliente.informeFinal))
            obj_cliente.save()

            #nueva_proyecto = proyecto(nombre=nombre, foto=foto)
            #messages.success(request,'Categoría añadida correctamente.')
            return redirect('clientes')
        else:
            messages.warning(request,'Faltan datos por introducir.')
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
    
    return redirect('empresa/cliente.html')