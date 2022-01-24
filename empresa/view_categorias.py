from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from Grupo11_PSP_RA6.settings import MEDIA_ROOT
from empresa.models import Categoria
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import CategoriaModelForm
from django.contrib import messages
import os


def mostrar_categorias(request):
    listCategorias = Categoria.objects.all()
    context = { 'categorias':listCategorias }
    return render(request,'empresa/categorias.html',context)


def datos_categoria(request,id):
    categoria = Categoria.objects.get(id = id)
    context = {'categoria':categoria}
    return render(request,'empresa/datos_categoria.html',context)


def annadir_categorias(request):
    categoria = CategoriaModelForm()
    context = {'categoria':categoria}

    if request.POST:
        categoria = CategoriaModelForm(request.POST, request.FILES)
        context = {'categoria': categoria}
        
        if categoria.is_valid():
            nombre = request.POST.get("nombre")
            foto = request.FILES.get("foto")

            if nombre is not None or foto is not None:
                nueva_categoria = Categoria(nombre=nombre, foto=foto)
                nueva_categoria.save()
                messages.success(request,'Categoría añadida correctamente.')
                return redirect('categorias')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_add_categoria')

    return render(request, "empresa/form_add_categoria.html",context)


"""def editar_categorias(request,id):
    id_categoria = Categoria.objects.get(pk=id)
    print("ID: "+str(id_categoria))
    #categoria = CategoriaModelForm(instance=id_categoria) # el error viene del forms.py
    #print("Categoría: "+str(categoria))
    
    #categoria = CategoriaModelForm(instance = id_categoria)
    #print("Test: "+str(categoria))
    
    context = {'categoria':id_categoria}
    
    return render(request, "empresa/form_edit_categoria.html",context)"""


"""def editar_categorias(request,id_categoria):
    id_cat = Categoria.objects.get(pk=id_categoria)
    #error = get_object_or_404(Categoria, id_cat)
    
    context = {'categoria':id_categoria}
    
    categoria = CategoriaModelForm(request.POST, request.FILES, instance = )
    
    if categoria.is_valid():
        nombre = request.POST.get("nombre")
        foto = request.FILES.get("foto")

        if nombre is not None or foto is not None:
            nueva_categoria = Categoria(nombre=nombre, foto=foto)
            nueva_categoria.save()
            messages.success(request,'Categoría añadida correctamente.')
            return redirect('categorias')
    else:
        messages.warning(request,'Faltan datos por introducir.')
        return redirect('form_edit_categoria')
    
    return render(request, "empresa/form_edit_categoria.html",context)"""


def editar_categorias(request,id):
    id_categoria = Categoria.objects.get(pk=id)
    
    categoria = CategoriaModelForm(instance=id_categoria)
    # 'id':id_categoria
    context = {'categoria':categoria}
    
    if request.method == 'POST':
        categoria = CategoriaModelForm(request.POST, request.FILES, instance=id_categoria)
        context = {'categoria':categoria}
        
        if categoria.is_valid():
            nombre = request.POST.get("nombre")
            foto = request.FILES.get("foto")
            
            if nombre is not None or foto is not None:
                set_categoria = Categoria(nombre=nombre, foto=foto)
                set_categoria.save()
                messages.success(request,'Categoría editada correctamente.')
                return redirect('categorias')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_edit_categoria')
        
    return render(request, "empresa/form_edit_categoria.html",context)


def eliminar_categorias(request,id):
    categoria = Categoria.objects.get(id=id)
    #categoria.delete()
    
    foto_categoria = Categoria.objects.filter(id=id).values_list('foto',flat=True)
    
    for imagen in foto_categoria:
        print(imagen)
        #os.remove(os.path.join(str(imagen))) # para auto eliminar la imágen del directorio#
    
    listCategorias = Categoria.objects.all()# para volver a mostrarlos todos#
    context = {'categorias':listCategorias}
    
    messages.error(request,'Categoria eliminada éxitosamente.')
    return render(request,'empresa/categorias.html',context)