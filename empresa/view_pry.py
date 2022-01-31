from datetime import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from empresa.models import Categoria, Empleado, Proyecto, Usuario
from .forms import CategoriaModelForm, EmpleadoModelForm, ProyectoModelForm, UsuarioModelForm
from django.contrib.auth.models import User
from django.contrib import messages


def mostrar_pry(request):
    listProyectos = Proyecto.objects.all()
    listEmpleados = Empleado.objects.all()
    
    context = {'empleados':listEmpleados, 'proyectos': listProyectos }
    return render(request,'empresa/proyectos.html',context)

def annadir_proyecto(request,empleado_id):
    id_emp = Empleado.objects.get(id=empleado_id)
        
    categorias = Categoria.objects.order_by('id').all()
    print("Categorias mostradas:\n"+str(categorias))
    
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
        
        if usuario.is_valid():
            username = request.POST['username']
            pwd = request.POST['password']
            
            usuario_pry = Usuario(username=username, password=pwd)
            usuario_pry.password = make_password(usuario_pry.password)
            usuario_pry.save()
            user = User.objects.create_user(username = username, password = pwd)
            user.save()
            
            if empleado.is_valid() and categoria.is_valid():
                last_id_usuario = Usuario.objects.last()
                emp_id = request.POST.get("id")
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellidos = request.POST.get("apellidos")
                direccion = request.POST.get("direccion")
                biografia = request.POST.get("biografia")
                idUsuario = request.POST.get("idUsuario",last_id_usuario)
                
                empleado_pry = Empleado(id=emp_id, dni=dni, nombre=nombre, apellidos=apellidos,
                    direccion=direccion, biografia=biografia, idUsuario=idUsuario)
                empleado_pry.save()
                
                id_cat = request.POST.get("id")
                nombre = request.POST.get("nombre")
                foto = request.FILES.get("foto")
                
                categoria_pry = Categoria(id=id_cat, nombre=nombre, foto=foto)
                categoria.save()
                
                if empleado.save() != None and categoria.save() != None:
                    if proyecto.is_valid():
                        titulo = request.POST.get("titulo")
                        descripcion = request.POST.get("descripcion")
                        nivel = request.POST.get("nivel")
                        fechaInicio = request.POST.get("fechaInicio")
                        fechaFin = request.POST.get("fechaFin")
                        informeFinal = request.POST.get("informeFinal")
                        idEmpleado = request.POST.get("idEmpleado",id_emp)
                        idCategoria  = request.POST.get("idCategoria",id_cat)

                        if titulo is not None or descripcion is not None or nivel is not None or fechaInicio is not None or fechaFin is not None or informeFinal is not None or idEmpleado or idCategoria is not None:
                            nuevo_proyecto = Proyecto(titulo=titulo, descripcion=descripcion, nivel=nivel, fechaInicio=fechaInicio,
                            fechaFin=fechaFin,informeFinal=informeFinal,idEmpleado=empleado_pry, idCategoria=categoria_pry)
                            nuevo_proyecto.save()
                            messages.success(request,'Proyecto añadido correctamente.')
                            return reverse('proyectos')

    return render(request, "empresa/form_add_pry.html",context)


def ver_historial_proyectos(request, idUsuario):
    id_usuario = Usuario.objects.filter(id=idUsuario)
    
    # Visualizamos solamente proyectos con fecha final igual a la actual (con formato dd/mm/YYYY) #
    fecha = datetime.now().strftime("%d/%m/%Y")
    #print("Fecha actual: "+str(fecha))
        
    #fecha_actual = datetime.strftime("%Y-%m-%d")
    print("Fecha actual: "+str(fecha))
    
    historial_proyectos = Proyecto.objects.order_by('-fechaInicio').all() #ordenamos por fecha final#
    
    context = { 'proyectos': historial_proyectos, 'usuario':id_usuario, 'fechaActual':fecha }
      
    return render(request,'empresa/historial_pry.html',context)


def annadir_inscripcion(request, idUsuario):
    id_usuario = Usuario.objects.filter(id=idUsuario)
    print(id_usuario)
    
    proyecto = ProyectoModelForm()
    context = {'proyecto': proyecto, 'usuario':id_usuario}

    if request.POST:
        proyecto = ProyectoModelForm(request.POST)
        context = {'proyecto': proyecto, 'usuario':id_usuario}
        
        if proyecto.is_valid():
            last_id_categoria = Categoria.objects.last()
            last_id_empleado = Empleado.objects.last()
            titulo = request.POST.get("titulo")
            descripcion = request.POST.get("descripcion")
            nivel = request.POST.get("nivel")
            fechaInicio = request.POST.get("fechaInicio")
            fechaFin = request.POST.get("fechaFin")
            informeFinal = request.POST.get("informeFinal")
            idCategoria  = request.POST.get("idCategoria",last_id_categoria)
            idEmpleado = request.POST.get("idEmpleado",last_id_empleado)

            if titulo is not None or descripcion is not None or nivel is not None or fechaInicio is not None or fechaFin is not None or informeFinal is not None or idCategoria or idEmpleado:
                inscripcion = Proyecto(titulo=titulo, descripcion=descripcion, nivel=nivel,
                fechaInicio=fechaInicio,fechaFin=fechaFin,informeFinal=informeFinal,
                idEmpleado=idEmpleado, idCategoria=idCategoria)
                inscripcion.save()
                messages.success(request,'Se ha inscrito al proyecto correctamente.')
                return redirect('historial_pry')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('inscripcion_pry')

    return render(request, "empresa/inscripcion_pry.html",context)