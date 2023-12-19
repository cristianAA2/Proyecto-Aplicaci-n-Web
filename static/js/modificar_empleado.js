document.addEventListener('DOMContentLoaded', function () {
    var table = document.getElementById('empleados-table');

    table.addEventListener('click', function (event) {
        var target = event.target;

        if (target.classList.contains('btn-edit')) {
            var rut = target.getAttribute('data-rut');
            var nombreElement = document.querySelector('td[data-field="nombre"][data-rut="' + rut + '"]');
            var apellidoElement = document.querySelector('td[data-field="apellido"][data-rut="' + rut + '"]');

            var newNombre = prompt('Nuevo nombre:', nombreElement.textContent);
            var newApellido = prompt('Nuevo apellido:', apellidoElement.textContent);

            if (newNombre !== null && newApellido !== null) {
                // Realizar la actualización AJAX
                fetch('/modificar_empleado/' + rut + '/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    body: 'nombre=' + encodeURIComponent(newNombre) + '&apellido=' + encodeURIComponent(newApellido)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Actualizar los valores en la tabla
                        nombreElement.textContent = newNombre;
                        apellidoElement.textContent = newApellido;
                    } else {
                        alert('Error al actualizar los datos.');
                    }
                });
            }
        }
    });
});