alert('Prueba de empleado');

eliminarEmpleado(id) {
    Swal.fire({
        title: '¿Desea eliminar el empleado ' + id + '?',
        text: "Empleado",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Mensaje de Salesemp!'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'Mensaje de Salesemp!',
                '¡¡Empleado eliminado éxitosamente!!',
                'success'
            );
        } else {
            Swal.fire(
                'Mensaje de Salesemp!',
                'No has eliminado a este empleado',
                'warning'
            );
        }
    });
}