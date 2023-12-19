function validarFormulario() {
    var nombre = document.getElementById('nombre').value;
    var apellido = document.getElementById('apellido').value;
    var fono = document.getElementById('fono').value;

    var hora = document.getElementById('hora').value;
    var fecha = document.getElementById('fecha').value;

    var correo = document.getElementById('id_cliente').value;
    var servicio = document.getElementById('id_servicio').value;
    var empleado = document.getElementById('rut_e').value;

    //Validar Nombre
    if (nombre.length < 3 || nombre.length > 20) {
        document.getElementById('nombre_msj').innerHTML = 'El nombre debe tener entre 3 y 20 caracteres.';
        return false;
        
    } else {
        document.getElementById('nombre_msj').innerHTML = '';
    }

    //Validar Apellido
    if (apellido.length < 3 || apellido.length > 20) {
        document.getElementById('apellido_msj').innerHTML = 'El apellido debe tener entre 3 y 20 caracteres.';
        return false;
    } else {
        document.getElementById('apellido_msj').innerHTML = '';
    }

    //Validar Correo
    if (!validarCorreo(correo)) {
        document.getElementById('correo_msj').innerHTML = 'Ingrese un correo electrónico válido.';
        return false;
    } else {
        document.getElementById('correo_msj').innerHTML = '';
    }

    //Validar Telefono
    if (!validarfono(fono)) {
        document.getElementById('fono_msj').innerHTML = 'Ingrese un número de teléfono válido.';
        return false;
    } else {
        document.getElementById('fono_msj').innerHTML = '';
    }

    //Validar Servicio
    if (servicio === 'Elija una opcion') {
        document.getElementById('servicio_msj').innerHTML = 'Seleccione un servicio válido.';
        return false;
    } else {
        document.getElementById('servicio_msj').innerHTML = '';
    }

    //Validar Empleado
    if (empleado ==='Seleccione un Empleado'){
        document.getElementById('empleado_msj').innerHTML = 'Debe seleccionar un empleado.';
        return false;
    } else {
        document.getElementById('empleado_msj').innerHTML = '';
    }


}

function validarCorreo(correo) {
    var regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regexCorreo.test(correo);
}

function validarfono(fono) {
    var regexfono = /^\d+([\s\-]?\d+)*$/;
    return regexfono.test(fono);
}

var imagenes = document.querySelectorAll('.imagen-container img');
var index = 0;

function cambiarImagen() {
    imagenes[index].style.opacity = 0;
    index = (index + 1) % imagenes.length;
    imagenes[index].style.opacity = 1;
}
setInterval(cambiarImagen, 5000);