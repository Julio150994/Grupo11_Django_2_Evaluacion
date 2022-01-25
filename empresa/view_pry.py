from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Empleado, Proyecto
from .forms import ProyectoModelForm
from django.contrib import messages

def mostrar_pry(request):
    listProyectos = Proyecto.objects.all()
    context = { 'proyectos': listProyectos }
    return render(request,'empresa/proyectos.html',context)

def annadir_proyecto(request):
    proyecto = ProyectoModelForm()
    context = {'proyecto': proyecto}

    if request.POST:
        proyecto = ProyectoModelForm(request.POST)
        context = {'proyecto': proyecto}
        
        if proyecto.is_valid():
            last_id_categoria = Categoria.objects.last()
            last_id_empresario = Empleado.objects.last()
            titulo = request.POST.get("titulo")
            descripcion = request.POST.get("descripcion")
            nivel = request.POST.get("nivel")
            fechaInicio = request.POST.get("fechaInicio")
            fechaFin = request.POST.get("fechaFin")
            informeFinal = request.POST.get("informeFinal")
            idCategoria  = request.POST.get("idCategoria",last_id_categoria)
            idEmpleado = request.POST.get("idEmpleado",last_id_empresario)

            if titulo is not None or descripcion is not None or nivel is not None or fechaInicio is not None or fechaFin is not None or informeFinal is not None or idCategoria or idEmpleado:
                nuevo_proyecto = Proyecto(titulo=titulo, descripcion=descripcion, nivel=nivel,
                fechaInicio=fechaInicio,fechaFin=fechaFin,informeFinal=informeFinal,
                idCategoria=idCategoria, idEmpleado=idEmpleado)
                nuevo_proyecto.save()
                messages.success(request,'Proyecto añadido correctamente.')
                return redirect('proyectos')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_add_pry')

    return render(request, "empresa/form_add_pry.html",context)


def ver_historial_proyectos(request):
    historialProyectos = Proyecto.objects.all()
    context = { 'proyectos': historialProyectos }
    return render(request,'empresa/historial_proyectos.html',context)

def annadir_inscripcion(request):
    proyecto = ProyectoModelForm()
    context = {'proyecto': proyecto}

    if request.POST:
        proyecto = ProyectoModelForm(request.POST)
        context = {'proyecto': proyecto}
        
        if proyecto.is_valid():
            last_id_categoria = Categoria.objects.last()
            last_id_empresario = Empleado.objects.last()
            titulo = request.POST.get("titulo")
            descripcion = request.POST.get("descripcion")
            nivel = request.POST.get("nivel")
            fechaInicio = request.POST.get("fechaInicio")
            fechaFin = request.POST.get("fechaFin")
            informeFinal = request.POST.get("informeFinal")
            idCategoria  = request.POST.get("idCategoria",last_id_categoria)
            idEmpleado = request.POST.get("idEmpleado",last_id_empresario)

            if titulo is not None or descripcion is not None or nivel is not None or fechaInicio is not None or fechaFin is not None or informeFinal is not None or idCategoria or idEmpleado:
                nuevo_proyecto = Proyecto(titulo=titulo, descripcion=descripcion, nivel=nivel,
                fechaInicio=fechaInicio,fechaFin=fechaFin,informeFinal=informeFinal,
                idCategoria=idCategoria, idEmpleado=idEmpleado)
                nuevo_proyecto.save()
                messages.success(request,'Se ha inscrito al proyecto correctamente.')
                return redirect('historial_pry')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('inscripcion_proyecto')

    return render(request, "empresa/inscripcion_proyecto.html",context)