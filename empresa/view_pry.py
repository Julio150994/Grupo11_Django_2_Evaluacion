from datetime import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from empresa.models import Categoria, Empleado, Participa, Proyecto, Usuario
from .forms import CategoriaModelForm, EmpleadoModelForm, ProyectoModelForm, UsuarioModelForm
from django.contrib import messages


def mostrar_pry(request):
    listProyectos = Proyecto.objects.all()
    listEmpleados = Empleado.objects.all()
    
    context = {'empleados':listEmpleados, 'proyectos': listProyectos }
    return render(request,'empresa/proyectos.html',context)

def annadir_proyecto(request,empleado_id):
    id_emp = Empleado.objects.get(id=empleado_id)
        
    categorias = Categoria.objects.order_by('id').all()
    
    usuario = UsuarioModelForm()
    empleado = EmpleadoModelForm()
    categoria = CategoriaModelForm()
    proyecto = ProyectoModelForm()
    
    context = {
        'empleado':id_emp,
        'categorias':categorias,
        'usuario':usuario,
        'emp':empleado,
        'categoria':categoria,
        'proyecto':proyecto
    }
    
    if request.POST:
        usuario = UsuarioModelForm(request.POST)
        empleado = EmpleadoModelForm(request.POST)
        categoria = CategoriaModelForm(request.POST,request.FILES)
        proyecto = ProyectoModelForm(request.POST)
        
        context = {
            'empleado':id_emp,
            'categorias':categorias,
            'usuario':usuario,
            'emp':empleado,
            'categoria':categoria,
            'proyecto':proyecto
        }
        
        if proyecto.is_valid():
            titulo = request.POST.get("titulo")
            descripcion = request.POST.get("descripcion")
            nivel = request.POST.get("nivel")
            fechaInicio = request.POST.get("fechaInicio")
            fechaFin = request.POST.get("fechaFin")
            informeFinal = request.POST.get("informeFinal")
            idEmpleado = request.POST.get("idEmpleado",id_emp)
            idCategoria = request.POST.get("idCategoria")

            if titulo is not None or descripcion is not None or nivel is not None or fechaInicio is not None or fechaFin is not None or informeFinal is not None or idEmpleado or idCategoria is not None:
                nuevo_proyecto = Proyecto(titulo=titulo, descripcion=descripcion, nivel=nivel, fechaInicio=fechaInicio,
                fechaFin=fechaFin,informeFinal=informeFinal,idEmpleado=idEmpleado, idCategoria=Categoria.objects.get(id=idCategoria))
                nuevo_proyecto.save()
                messages.success(request,'Proyecto añadido correctamente.')
                return redirect('proyectos')
            
    return render(request, "empresa/form_add_pry.html",context)


def modificar_pry(request,id,empleado_id):
    id_proyecto = Proyecto.objects.get(id = id)
    id_emp = Empleado.objects.get(id = empleado_id)
        
    categorias = Categoria.objects.order_by('id').all()
    
    context = {
        'proyecto':id_proyecto,
        'empleado':id_emp,
        'categorias':categorias
    }
    
    if request.POST:
        proyecto = ProyectoModelForm(request.POST, instance=id_proyecto)
        
        context = {
            'proyecto':proyecto,
            'empleado':id_emp,
            'categorias':categorias
        }
        
        if proyecto.is_valid():
            titulo = request.POST.get("titulo")
            descripcion = request.POST.get("descripcion")
            nivel = request.POST.get("nivel")
            fechaInicio = request.POST.get("fechaInicio")
            fechaFin = request.POST.get("fechaFin")
            informeFinal = request.POST.get("informeFinal")
            idEmpleado = request.POST.get("idEmpleado",id_emp)
            idCategoria  = request.POST.get("idCategoria")

            if titulo is not None or descripcion is not None or nivel is not None or fechaInicio is not None or fechaFin is not None or informeFinal is not None or idEmpleado or idCategoria is not None:
                modificar_pry = Proyecto(titulo=titulo, descripcion=descripcion, nivel=nivel, fechaInicio=fechaInicio,
                fechaFin=fechaFin,informeFinal=informeFinal,idEmpleado=idEmpleado, idCategoria=Categoria.objects.get(id=idCategoria))
                modificar_pry.save()
                messages.info(request,'Proyecto modificado correctamente.')
                return redirect('proyectos')
            
    return render(request, "empresa/form_edit_pry.html",context)


def dar_baja_pry(request,id):
    proyecto = Proyecto.objects.filter(id=id)
    proyecto.delete()
    
    listProyectos = Proyecto.objects.order_by('-fechaInicio').all()
    context = {'proyectos':listProyectos}
    
    messages.error(request,'Ha podido darse de baja correctamente.')
    return render(request,"empresa/proyectos.html",context)


def ver_historial_proyectos(request, idUsuario):
    id_usuario = Usuario.objects.filter(id=idUsuario)
    
    # Visualizamos solamente proyectos con fecha final igual a la actual (con formato dd/mm/YYYY) #
    fecha = datetime.now().strftime("%d/%m/%Y")
    #print("Fecha actual: "+str(fecha))
        
    #fecha_actual = datetime.strftime("%Y-%m-%d")
    print("Fecha actual: "+str(fecha))
    
    historial_proyectos = Proyecto.objects.order_by('fechaInicio').all() #ordenamos por fecha final#
    
    context = { 'proyectos': historial_proyectos, 'usuario':id_usuario, 'fechaActual':fecha }
      
    return render(request,'empresa/historial_pry.html',context)
