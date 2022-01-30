function eliminar(id) {
    Swal.fire({
        title: 'Mensaje de Salesemp',
        text: "¿Desea eliminar este empleado?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#076BCA',
        cancelButtonColor: '#C62D00',
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((empleado) => {
        if (empleado.isConfirmed) {
            window.location = '/eliminar_empleado/' + id;
        } else {
            window.location = '/empleados';
        }
    });
}