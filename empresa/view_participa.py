from datetime import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Empleado, Participa, Proyecto, Usuario
from .forms import EmpleadoModelForm, ProyectoModelForm
from django.contrib import messages

def mostrar_clientes_pry(request,idEmpleado):
    id_empleado = Empleado.objects.filter(id=idEmpleado)
    print("Id de empleado: "+str(id_empleado))
    
    listParticipas = Participa.objects.order_by('-id').all()
    context = { 'participas': listParticipas }
    return render(request,'empresa/proyectos_emp.html',context)