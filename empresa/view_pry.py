from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Proyecto
from .forms import ProyectoModelForm
from django.contrib import messages

def mostrar_pry(request):
    listProyectos = Proyecto.objects.all()
    context = { 'proyectos': listProyectos }
    return render(request,'empresa/proyectos.html',context)

def annadir_proyecto(request):
    proyecto = ProyectoModelForm()
    context = {'proyecto':proyecto}

    if request.method == 'POST':
        proyecto = ProyectoModelForm(request.POST, request.FILES)
        context = {'proyecto': proyecto}
        
        if proyecto.is_valid():
            obj_proyecto = proyecto.objects.get(pk=id)
            obj_proyecto.titulo = proyecto.cleaned_data['titulo']
            print("titulo: "+str(obj_proyecto.titulo))
            obj_proyecto.descripcion = proyecto.cleaned_data['descripcion']
            print("descripcion: "+str(obj_proyecto.descripcion))
            obj_proyecto.nivel = proyecto.cleaned_data['nivel']
            print("nivel: "+str(obj_proyecto.nivel))
            obj_proyecto.fechaInicio = proyecto.cleaned_data['fechaInicio']
            print("fechaInicio: "+str(obj_proyecto.fechaInicio))
            obj_proyecto.fechaFin = proyecto.cleaned_data['fechaFin']
            print("fechaFin: "+str(obj_proyecto.fechaFin))
            obj_proyecto.informeFinal = proyecto.cleaned_data['informeFinal']
            print("informeFinal: "+str(obj_proyecto.informeFinal))
            obj_proyecto.save()

            #nueva_proyecto = proyecto(nombre=nombre, foto=foto)
            #messages.success(request,'Categoría añadida correctamente.')
            return redirect('proyectos')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_add_pry')

    return render(request, "empresa/form_add_pry.html",context)