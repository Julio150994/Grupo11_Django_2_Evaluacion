from datetime import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Cliente, Empleado, Participa, Proyecto, Usuario
from .forms import CategoriaModelForm, ClienteModelForm, ParticipaModelForm, UsuarioModelForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.views.generic import View


def mostrar_clientes_pry(request,id):
    proyecto = Proyecto.objects.get(id = id)
    print("Id proyecto: "+str(proyecto))
    
    #id_emp = Empleado.objects.get(id = empleado_id)
    
    listPryClientes = Participa.objects.order_by('-id').all() #primero visualizar los clientes en proyectos del empleado#
    context = {'proyecto':proyecto, 'participas':listPryClientes}
    
    return render(request,"empresa/ver_clientes_empleado.html",context)


def annadir_inscripcion_pry(request, cliente_id):
    id_cliente = Cliente.objects.get(id=cliente_id)
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    proyectos = Proyecto.objects.order_by('id').all()
    
    usuario = UsuarioModelForm()
    cliente = ClienteModelForm()
    categoria = CategoriaModelForm()
    participa = ParticipaModelForm()
    context = {
        'cliente':id_cliente,
        'proyectos':proyectos,
        'usuario':usuario,
        'cli':cliente,
        'categoria':categoria,
        'participa': participa
    }

    if request.POST:
        usuario = UsuarioModelForm(request.POST)
        cliente = ClienteModelForm(request.POST)
        categoria = CategoriaModelForm(request.POST,request.FILES)
        participa = ParticipaModelForm(request.POST)
        context = {
            'cliente':id_cliente,
            'proyectos':proyectos,
            'usuario':usuario,
            'cli':cliente,
            'categoria':categoria,
            'participa': participa
        }
        
        if participa.is_valid():
            idCliente = request.POST.get("idCliente",id_cliente)
            idProyecto = request.POST.get("idProyecto")
            fechaInscripcion = request.POST.get("fechaInscripcion")
            rol = request.POST.get("rol")
            
            # Realizamos la comprobación de fechas #
            if fechaInscripcion < fecha_actual:
                if idCliente is not None or idProyecto is not None or fechaInscripcion is not None or rol is not None:
                    participa_pry = Participa(idCliente=idCliente, idProyecto=Proyecto.objects.get(id=idProyecto), fechaInscripcion=fechaInscripcion, rol=rol)
                    participa_pry.save()
                    messages.success(request,'Se ha inscrito al proyecto correctamente.')
                    return redirect('proyectos')
            else:
                messages.error(request,'La fecha de inscripción no puede realizarse hoy, ni posteriormente.')
                return redirect('inscripcion_pry')    
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('inscripcion_pry')

    return render(request, "empresa/inscripcion_pry.html",context)


def buscar_clientes_pry(request):
    nombre_rol = request.GET.get("search")
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    
    list_usuarios = Usuario.objects.all()
    list_empleados = Empleado.objects.all()
    list_proyectos = Proyecto.objects.all()
    list_clientes_emp = Participa.objects.all()
    
    context = {
        'usuarios':list_usuarios,
        'empleados':list_empleados,
        'proyectos':list_proyectos,
        'participas':list_clientes_emp,
        'fechaActual':fecha_actual
    }
    

    if nombre_rol:
        #__icontains = para evitar errores de tipo case sensitive#
        resultado = Participa.objects.filter(Q(rol__icontains=nombre_rol))
        
        context = {
            'usuarios':list_usuarios,
            'empleados':list_empleados,
            'proyectos':list_proyectos,
            'participas':resultado,
            'fechaActual':fecha_actual
        }
    
    return render(request,"empresa/buscar_clientes.html",context)

def mostrar_informe_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="datos_cliente.pdf"'

    #Utilizamos el almacenamiento temporal BytesIO#
    almacenamiento = BytesIO()
    #Utilizamos canvas para las coordenadas que nos sirven para situar cada elemento #
    dependencia = canvas.Canvas(almacenamiento)
    #self.header(cliente_pdf)
    #ejeY = 600
    #self.tabla(cliente_pdf, ejeY) <------- esto cuando funcione el informe PDF
    #cliente_pdf.showPage()
    #cliente_pdf.save()
    cliente_pdf = canvas.Canvas(response)
    logo_salesianos = settings.MEDIA_ROOT+'\logo_informe.png'
    cliente_pdf.drawImage(logo_salesianos, 40, 750, 120, 90, preserveAspectRatio=True)
    cliente_pdf.setFont("Helvetica", 16)
    cliente_pdf.drawString(230, 790, u"DATOS Y PROYECTOS DE CLIENTE")
    cliente_pdf.setFont("Helvetica", 14)
    cliente_pdf.showPage()
    cliente_pdf.save()
    
    #Utilizamos canvas para las coordenadas que nos sirven para situar cada elemento #
    #ejeY = 600
    #self.tabla(cliente_pdf, ejeY) <------- esto cuando funcione el informe PDF
    return response