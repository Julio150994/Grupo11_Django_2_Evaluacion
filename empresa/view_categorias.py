from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria
from .forms import CategoriaModelForm
from django.contrib import messages


def mostrar_categorias(request):
    listCategorias = Categoria.objects.all()
    context = { 'categorias':listCategorias }
    return render(request,'empresa/categorias.html',context)

def datos_categoria(request,id):
    categoria = Categoria.objects.get(id = id)
    context = {'categoria':categoria}
    return render(request,'empresa/datos_categoria.html',context)

def aniadir_categoria(request):
    categoria = CategoriaModelForm()
    context = {'categoria':categoria}

    if request.method == 'POST':
        categoria = CategoriaModelForm(request.POST, request.FILES)
        print("Imágen: "+str(request.FILES))
        context = {'categoria': categoria}
        
        if categoria.is_valid():
            obj_categoria = Categoria.objects.get(pk=id)
            obj_categoria.nombre = categoria.cleaned_data['nombre']
            print("Nombre: "+str(obj_categoria.nombre))
            obj_categoria.foto = categoria.cleaned_data['foto']
            print("Foto: "+str(obj_categoria.foto))
            obj_categoria.save()

            #nueva_categoria = Categoria(nombre=nombre, foto=foto)
            #messages.success(request,'Categoría añadida correctamente.')
            return redirect('categorias')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_add_categoria')

    return render(request, "empresa/form_add_categoria.html",context)

def editar_categoria(request,id):
    id_categoria = Categoria.objects.get(id = id)
    
    if request.method == 'GET':
        categoria = CategoriaModelForm(instance = id_categoria)
        context = {'categoria': categoria}
    else:
        categoria = CategoriaModelForm(request.POST, request.FILES, instance = id_categoria)
        context = {'categoria': categoria}
            
        if categoria.is_valid():
            categoria.save()
            #messages.success(request,'Categoría editada correctamente.')
            return reverse(redirect('categorias')+"?cat_updated")
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_edit_categoria')
    
    return render(request, "empresa/form_edit_categoria.html",context)

def eliminar_categoria(request,id):
    categoria = Categoria.objects.get(id = id)
    context = {'categoria':categoria}
    
    if categoria is None:
        messages.warning(request,'No se ha podido eliminar esta categoria.')
    else:
        categoria.delete()
        messages.error(request,'Categoria '+str(categoria)+' eliminada éxitosamente.')
    
    return render(request,'empresa/categorias.html',context)