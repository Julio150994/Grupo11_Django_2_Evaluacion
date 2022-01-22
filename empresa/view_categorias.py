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


def editar_categorias(request,id):
    id_categoria = Categoria.objects.get(id = id)
    print("ID: "+str(id_categoria))
    #categoria = CategoriaModelForm(instance=id_categoria) # el error viene del forms.py
    #print("Categoría: "+str(categoria))
    
    #categoria = CategoriaModelForm(instance = id_categoria)
    #print("Test: "+str(categoria))
    
    context = {'categoria':id_categoria}
    
    return render(request, "empresa/form_edit_categoria.html",context)


"""def editar_categorias(request,id):
    id_categoria = Categoria.objects.get(id = id)
   
    if request.method == 'GET':
        categoria = CategoriaModelForm(instance=id_categoria)
        context = {'categoria':categoria}
    else:
        categoria = CategoriaModelForm(request.POST, request.FILES, instance=id_categoria)
        context = {'categoria':categoria}
        
        if categoria.is_valid():
            categoria.save()
            messages.success(request,'Categoría editada correctamente.')
            return redirect('categorias')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_edit_categoria')
        
    return render(request, "empresa/form_edit_categoria.html",context)"""
   

"""def editar_categorias(request,id):
    id_categoria = Categoria.objects.get(id = id)
    print("Id: "+str(id_categoria))# llega
    
    categoria = CategoriaModelForm(instance = id_categoria)
    print("Test: "+str(categoria)) #llega
    context = {'categoria': categoria}
    print("P: "+str(context))
    
    print("P2: "+str(request.POST))
    print("P3: "+str(request.FILES))
    
    if request.POST:
        print("P4: "+str(request.POST))
        print("P5: "+str(request.FILES))
        
        categoria = CategoriaModelForm(request.POST, request.FILES, instance = id_categoria)
        print("Test 2: "+str(categoria))
        context = {'categoria': categoria}
            
        if categoria.is_valid():
            print("Prueba 2")
            nombre = request.POST.get("nombre")
            foto = request.FILES.get("foto")
            
            if nombre is not None or foto is not None:
                set_categoria = Categoria(nombre=nombre, foto=foto)
                print("Prueba 3")
                set_categoria.save()
                messages.success(request,'Categoría editada correctamente.')
                return redirect('categorias')
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('form_edit_categoria')
    
    return render(request, "empresa/form_edit_categoria.html",context)"""


def eliminar_categorias(request,id):
    categoria = Categoria.objects.get(id = id)
    context = {'categoria':categoria}
    
    if categoria is None:
        messages.warning(request,'No se ha podido eliminar esta categoria.')
    else:
        categoria.delete()
        messages.error(request,'Categoria '+str(categoria)+' eliminada éxitosamente.')
    
    return render(request,'empresa/categorias.html',context)