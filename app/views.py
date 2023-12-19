from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from app.models import Servicio, Cliente, Empleado, Atencion
from django.shortcuts import get_object_or_404,render
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    """
    @brief Renderiza la página principal de la aplicación.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página principal.
    """
    return render(request, 'app/index.html')

def nosotros(request):
    """
    @brief Renderiza la página "Nosotros" de la aplicación.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página "Nosotros".
    """
    return render(request, 'app/nosotros.html')

def servicios(request):
    """
    @brief Renderiza la página de servicios de la aplicación.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página de servicios.
    """
    serv = Servicio.objects.all()
    data = {'servicios': serv}
    return render(request, 'app/servicios.html', data)

def login_view(request):
    """
    @brief Maneja la autenticación de usuario.

    Si recibe un POST con credenciales válidas, redirige al dashboard.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página de inicio de sesión o redirección al dashboard.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
    return render(request, 'app/login.html')


def logout_view(request):
    """
    @brief Cierra la sesión del usuario y redirige a la página principal.

    @param request: Objeto de solicitud de Django.
    @return: Redirección a la página principal.
    """
    logout(request)
    return redirect('/')

def reservas(request):
    """
    @brief Renderiza la página de reservas y maneja la creación de nuevas reservas.

    También verifica la disponibilidad de fechas y horas.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página de reservas o redirección a la página de confirmación.

    @remark Si la solicitud es un POST, la función intentará crear una nueva reserva y redirigir a la página de confirmación.
    """
    # Obtener la fecha actual y configurar la fecha de finalización para la visualización de reservas de la próxima semana.
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=7)
    end_date = datetime.combine(end_date, datetime.max.time())
    
    # Obtener todos los servicios y empleados disponibles.
    servicios = Servicio.objects.all()
    empleados = Empleado.objects.all()

    # Configurar datos para la plantilla.
    data = {
        'servicios': servicios, 
        'empleados': empleados,
        'current_date': current_date,
        'end_date': end_date,
    }

    if request.method == 'POST':
        # Obtener datos del formulario POST.
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        id_cliente_value = request.POST.get('id_cliente')
        fono = request.POST.get('fono')
        id_servicio_value = request.POST.get('id_servicio')
        rut_e_value = request.POST.get('rut_e')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        # Crear o actualizar un cliente.
        cliente, created = Cliente.objects.get_or_create(
            id_cliente=id_cliente_value,
            defaults={'nombre': nombre, 'apellido': apellido, 'fono': fono}
        )
        if not created and cliente.nombre == '' and cliente.apellido == '' and cliente.fono == '':
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.fono = fono
            cliente.save()

        # Obtener un empleado y un servicio.
        empleado = get_object_or_404(Empleado, rut_e=rut_e_value)
        servicio = get_object_or_404(Servicio, id_servicio=id_servicio_value)

        # Verificar la disponibilidad de la fecha y hora seleccionadas.
        existing_reserva = Atencion.objects.filter(fecha=fecha, hora=hora).first()
        if existing_reserva:
            error_message = "Ya existe una reserva para la fecha y hora seleccionadas."
            data['error_message'] = error_message
            return render(request, 'app/reservas.html', data)
    
        # Crear la nueva reserva.
        atencion = Atencion(
            id_cliente=cliente,
            id_servicio=servicio,
            rut_e=empleado,
            fecha=fecha,
            hora=hora,
            estado='Pendiente',
            reserva=True
        )
        atencion.save()

        # Redirigir a la página de confirmación.
        return redirect('/confirmada')

    # Renderizar la página de reservas con los datos proporcionados.
    return render(request, 'app/reservas.html', data)

def dashboard(request):
    """
    @brief Renderiza la página de dashboard con la lista de reservas.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página de dashboard.
    """
    reserva = Atencion.objects.all()
    data = {'reservas': reserva}
    return render(request, 'app/dashboard.html', data)

def confirmada(request):
    """
    @brief Renderiza la página de confirmación.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página de confirmación.
    """
    return render(request, 'app/confirmada.html')

def aceptar(request, id_atencion):
    """
    @brief Cambia el estado de una reserva a 'Aceptado'.

    @param request: Objeto de solicitud de Django.
    @param id_atencion: Identificador único de la reserva.
    @return: Redirección a la página de dashboard.
    """
    try:
        reserva = Atencion.objects.get(id_atencion=id_atencion)
        reserva.estado = 'Aceptado'
        reserva.save()
    except Atencion.DoesNotExist:
        print("La atención no existe.")
    
    return redirect('/dashboard/')

def cancelar(request, id_atencion):
    """
    @brief Cambia el estado de una reserva a 'Cancelado'.

    @param request: Objeto de solicitud de Django.
    @param id_atencion: Identificador único de la reserva.
    @return: Redirección a la página de dashboard.
    """
    try:
        reserva = Atencion.objects.get(id_atencion=id_atencion)
        reserva.estado = 'Cancelado'
        reserva.save()
    except Atencion.DoesNotExist:
        print("La atención no existe.")
    return redirect('/dashboard/')

def eliminar(request, id_atencion):
    """
    @brief Elimina una reserva.

    @param request: Objeto de solicitud de Django.
    @param id_atencion: Identificador único de la reserva.
    @return: Redirección a la página de dashboard.
    """
    try:
        reserva = Atencion.objects.get(id_atencion=id_atencion)
        reserva.delete()
    except Atencion.DoesNotExist:
        print("La atención no existe.")
    return redirect('/dashboard/')

def detalle(request, id_atencion):
    """
    @brief Renderiza la página de detalle de una reserva.

    @param request: Objeto de solicitud de Django.
    @param id_atencion: Identificador único de la reserva.
    @return: Respuesta renderizada para la página de detalle.
    """
    try:
        reserva = Atencion.objects.get(id_atencion=id_atencion)
        data = {'reserva': reserva}
        return render(request, 'app/detalle.html', data)
    except Atencion.DoesNotExist:
        print("La atención no existe.")

def dashboardEmp(request):
    """
    @brief Renderiza la página de dashboard de empleados con la lista de empleados.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página de dashboard de empleados.
    """
    empleados = Empleado.objects.all()
    data = {'empleados': empleados}
    return render(request, 'app/dashboardEmp.html', data)

def agregar_empleado(request):
    """
    @brief Agrega un nuevo empleado.

    @param request: Objeto de solicitud de Django.
    @return: Redirección a la página de dashboard de empleados después de agregar un empleado.

    @remark Si la solicitud es un POST, la función intentará agregar un nuevo empleado con la información proporcionada.
    """
    if request.method == 'POST':
        rut_e = request.POST['rut_e']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']

        nuevo_empleado = Empleado(
            rut_e=rut_e,
            nombre=nombre,
            apellido=apellido,
        )
        nuevo_empleado.save()
        return redirect('dashboardEmp')
    
    return render(request, 'app/agregar_empleado.html')

def editar_empleado(request, rut_e):
    """
    @brief Edita la información de un empleado existente.

    @param request: Objeto de solicitud de Django.
    @param rut_e: Rut único del empleado que se desea editar.
    @return: Redirección a la página de dashboard de empleados después de editar un empleado.

    @remark Si la solicitud es un POST, la función intentará actualizar la información del empleado con la información proporcionada.
    """
    empleado = get_object_or_404(Empleado, rut_e=rut_e)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido = request.POST.get('apellido')
        empleado.save()
        return redirect('dashboardEmp')
    
    return render(request, 'app/editar_empleado.html', {'empleado': empleado})

def dashboardServ(request):
    """
    @brief Renderiza la página de dashboard de servicios con la lista de servicios.

    @param request: Objeto de solicitud de Django.
    @return: Respuesta renderizada para la página de dashboard de servicios.
    """
    servicios = Servicio.objects.all()
    data = {'servicios': servicios}
    return render(request, 'app/dashboardServ.html', data)

def agregar_servicio(request):
    """
    @brief Agrega un nuevo servicio.

    @param request: Objeto de solicitud de Django.
    @return: Redirección a la página de dashboard de servicios después de agregar un servicio.

    @remark Si la solicitud es un POST, la función intentará agregar un nuevo servicio con la información proporcionada.
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        descripcion = request.POST.get('descripcion', '')
        imagen = request.FILES['imagen']

        nuevo_servicio = Servicio(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            imagen=imagen
        )
        nuevo_servicio.save()
        return redirect('dashboardServ')
    
    return render(request, 'app/agregar_servicio.html')

def editar_servicio(request, servicio_id):
    """
    @brief Edita la información de un servicio existente.

    @param request: Objeto de solicitud de Django.
    @param servicio_id: Identificador único del servicio que se desea editar.
    @return: Redirección a la página de dashboard de servicios después de editar un servicio.

    @remark Si la solicitud es un POST, la función intentará actualizar la información del servicio con la información proporcionada.
    """
    servicio = get_object_or_404(Servicio, id_servicio=servicio_id)

    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre')
        servicio.descripcion = request.POST.get('descripcion')
        servicio.precio = request.POST.get('precio')
        servicio.save()
        return redirect('dashboardServ')

    return render(request, 'app/editar_servicio.html', {'servicio': servicio})