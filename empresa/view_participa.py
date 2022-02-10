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
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
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


"""-------Métodos que realizan las funciones requeridas para nuestro informe PDF-------"""
def mostrar_informe_pdf(request, cliente_id):
    # Obtenemos el id del cliente con el que hemos iniciado sesión
    id_cliente = Cliente.objects.filter(id=cliente_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="datos_cliente.pdf"' #nombre del archivo descargado

    #almacenamiento = BytesIO()
    #dep_canvas = canvas.Canvas(almacenamiento)
   
    cliente_pdf = canvas.Canvas(response)
    logo_salesianos = settings.MEDIA_ROOT+'\logo_informe.png'
    cliente_pdf.drawImage(logo_salesianos, 20, 765, 40, 70, preserveAspectRatio=True)
    cliente_pdf.setFont("Helvetica", 18)
    cliente_pdf.drawString(195, 790, u"INFORME PDF DE SALESEMP")
    
    cliente_pdf.drawString(10, 690, u"DATOS DE CLIENTE") #cambiar el color de este texto
    #self.header(cliente_pdf)
    eje_y = 640
    tabla_datos_cliente(cliente_pdf, eje_y, id_cliente)
    
    cliente_pdf.showPage()
    cliente_pdf.save()
    
    #pdf = buffer.getvalue()
    #buffer.close()
    #response.write(pdf)
    return response


def tabla_datos_cliente(cliente_pdf, eje_y, id_cliente):
    campos = ("Dni","Nombre","Apellidos","Dirección","Fecha de Nacimiento","Fecha de Alta","Usuario")
    # Llamamos a los datos del cliente que estamos utilizando #
    # for cliente in Cliente.objects.all() #
    resultado = [(cliente.dni, cliente.nombre, cliente.apellidos, cliente.direccion,
                cliente.fechaNacimiento, cliente.fechaAlta, cliente.idUsuario.username) for cliente in id_cliente ]
    ver_tabla_cliente = Table([campos] + resultado) #colWidths=[5, 5, 5]#
    # Aplicamos estilos para nuestras celdas #
    ver_tabla_cliente.setStyle(TableStyle(
        [
            #Campos de tabla cliente#
            ('ALIGN',(0,0),(3,0),'CENTER'),
            ('GRID',(0,0), (-1, -1), 1, colors.red),
            ('FONTSIZE',(0, 0),(-1, -1), 10),
        ]
    ))
    
    ver_tabla_cliente.wrapOn(cliente_pdf, 500, 350) # anchura y altura de la tabla#
    ver_tabla_cliente.drawOn(cliente_pdf, 10, eje_y) # coordenada que se mostrará en la tabla#