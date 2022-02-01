from datetime import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Cliente, Empleado, Participa, Proyecto, Usuario
from .forms import CategoriaModelForm, ClienteModelForm, ParticipaModelForm, UsuarioModelForm
from django.contrib import messages


def mostrar_clientes_pry(request,id):
    proyecto = Proyecto.objects.get(id = id)
    print("Id proyecto: "+str(proyecto))
    
    #id_emp = Empleado.objects.get(id = empleado_id)
    
    listPryClientes = Participa.objects.order_by('-id').all() #primero visualizar los clientes en proyectos del empleado#
    context = {'proyecto':proyecto, 'participas':listPryClientes}
    
    return render(request,"empresa/ver_clientes_empleado.html",context)


def annadir_inscripcion_pry(request, cliente_id):
    id_cliente = Cliente.objects.get(id=cliente_id)
    
    proyectos = Proyecto.objects.order_by('id').all()
    
    usuario = UsuarioModelForm()
    cliente = ClienteModelForm()
    categoria = CategoriaModelForm()
    participa = ParticipaModelForm()
    context = {
        'cliente':id_cliente,
        'proyectos':proyectos,
        'usuario':usuario,
        'cli':cliente,
        'categoria':categoria,
        'participa': participa
    }

    if request.POST:
        usuario = UsuarioModelForm(request.POST)
        cliente = ClienteModelForm(request.POST)
        categoria = CategoriaModelForm(request.POST,request.FILES)
        participa = ParticipaModelForm(request.POST)
        context = {
            'cliente':id_cliente,
            'proyectos':proyectos,
            'usuario':usuario,
            'cli':cliente,
            'categoria':categoria,
            'participa': participa
        }
        
        if participa.is_valid():
            idCliente = request.POST.get("idCliente",id_cliente)
            idProyecto = request.POST.get("idProyecto")
            fechaInscripcion = request.POST.get("fechaInscripcion")
            rol = request.POST.get("rol")

            if idCliente is not None or idProyecto is not None or fechaInscripcion is not None or rol is not None:
                participa_pry = Participa(idCliente=idCliente, idProyecto=Proyecto.objects.get(idProyecto), fechaInscripcion=fechaInscripcion, rol=rol)
                participa_pry.save()
                messages.success(request,'Se ha inscrito al proyecto correctamente.')
                return redirect('page_inicio')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('inscripcion_pry')

    return render(request, "empresa/inscripcion_pry.html",context)