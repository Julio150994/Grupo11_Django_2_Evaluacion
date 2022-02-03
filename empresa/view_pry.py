import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Cliente, Empleado, Participa, Proyecto, Usuario
from .forms import CategoriaModelForm, EmpleadoModelForm, ProyectoModelForm, UsuarioModelForm
from django.contrib import messages
from django.db.models import Q

def mostrar_pry(request):
    list_usuarios = Usuario.objects.all()
    list_proyectos = Proyecto.objects.all()
    list_empleados = Empleado.objects.all()
    list_clientes = Cliente.objects.all()
    list_proyectos_cliente = Participa.objects.all()
    
    context = {
        'usuarios':list_usuarios,
        'empleados':list_empleados,
        'clientes':list_clientes,
        'proyectos': list_proyectos,
        'participas':list_proyectos_cliente
    }
    return render(request,'empresa/proyectos.html',context)


def mostrar_pry_clientes(request):
    nombre_categoria = request.GET.get("search")
    print("Nombre de categoría: "+str(nombre_categoria))
    
    list_usuarios = Usuario.objects.all()
    list_proyectos = Proyecto.objects.all()
    list_clientes = Cliente.objects.all()
    list_proyectos_cliente = Participa.objects.all()
    
    context = {
        'usuarios':list_usuarios,
        'clientes':list_clientes,
        'proyectos': list_proyectos,
        'participas':list_proyectos_cliente
    }
    
    if nombre_categoria:
        list_categorias = Categoria.objects.filter(nombre=nombre_categoria)
        print("Categorías: "+str(list_categorias))
        
        #__icontains: es para buscar por categoría, sin errores por Case Sensitive#

        list_categoria_proyecto = Participa.objects.filter(
            Q(list_categorias==nombre_categoria)
        )
        
        """list_categoria_proyecto = Participa.objects.filter(
            Q(idProyecto=Proyecto.objects.filter(
              Q(idCategoria=Categoria.objects.filter(
                  Q(nombre__icontains=nombre_categoria) | Q(nombre__icontains=nombre_categoria)
              ))
            ))
        )"""
        
        context = {
            'usuarios':list_usuarios,
            'clientes':list_clientes,
            'proyectos': list_proyectos,
            'participas':list_categoria_proyecto
        }
    
    return render(request,'empresa/proyectos_cliente.html',context)



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
    
    if request.method == 'POST':
        proyecto = ProyectoModelForm(request.POST, instance=id_proyecto)
        
        context = {
            'proyecto':proyecto,
            'categorias':categorias
        }
        
        if proyecto.is_valid():
            titulo = request.POST.get("titulo")
            descripcion = request.POST.get("descripcion")
            nivel = request.POST.get("nivel")
            fechaInicio = request.POST.get("fechaInicio")
            fechaFin = request.POST.get("fechaFin")
            informeFinal = request.POST.get("informeFinal")
            idCategoria  = request.POST.get("idCategoria")

            if titulo is not None or descripcion is not None or nivel is not None or fechaInicio is not None or fechaFin is not None or informeFinal is not None or idCategoria is not None:
                proyecto.save()
                messages.success(request,'Proyecto modificado correctamente.')
                return redirect('proyectos')
            
    
            
    return render(request, "empresa/form_edit_pry.html",context)


def dar_baja_pry(request,id):
    proyecto = Proyecto.objects.filter(id=id)
    proyecto.delete()
    
    messages.error(request,'Ha podido darse de baja correctamente.')
    return redirect('proyectos')


def ver_historial_proyectos(request, idUsuario):
    id_usuario = Usuario.objects.filter(id=idUsuario)
    
    fecha = datetime.now().strftime("%d/%m/%Y")
        
    historial_proyectos = Proyecto.objects.order_by('fechaInicio').all() #ordenamos por fecha final#
    
    context = { 'proyectos': historial_proyectos, 'usuario':id_usuario, 'fechaActual':fecha }
      
    return render(request,'empresa/historial_pry.html',context)


def proyectos_siguiente_lunes(request):
       
    today = datetime.date.today() # SE QUEDA EN INGLES PARA FACILITAR EL USO DE LA MISMA
    semana_Siguiente = today + datetime.timedelta(days=-today.weekday(),weeks=1) # DEVUELVE EL LUNES QUE VIENE
    semana_Que_Viene = today + datetime.timedelta(days=-today.weekday(),weeks=2) # DEVUELVE EL LUNES SIGUIENTE
    
    proyectos_semanales = Proyecto.objects.order_by('fechaInicio').filter(fechaInicio__gte=semana_Siguiente).filter(fechaInicio__lt=semana_Que_Viene)
    
    
    context = { 
        'proyectos': proyectos_semanales,
    }
    
    return render(request,'empresa/proyectos_Lunes.html',context)