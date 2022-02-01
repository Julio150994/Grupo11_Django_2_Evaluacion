from datetime import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Empleado, Participa, Proyecto, Usuario
from .forms import EmpleadoModelForm, ProyectoModelForm
from django.contrib import messages


def mostrar_clientes_pry(request,id):
    proyecto = Proyecto.objects.get(id = id)
    print("Id proyecto: "+str(proyecto))
    
    #id_emp = Empleado.objects.get(id = empleado_id)
    
    listPryClientes = Participa.objects.order_by('-id').all() #primero visualizar los clientes en proyectos del empleado#
    context = {'proyecto':proyecto, 'participas':listPryClientes}
    
    return render(request,"empresa/ver_clientes_empleado.html",context)