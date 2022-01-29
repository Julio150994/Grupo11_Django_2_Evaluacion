function eliminarEmpleado() {
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
            Swal.fire(
                'Mensaje',
                'Empleado eliminado correctamente',
                'success'
            )
        }
        else {
            Swal.fire(
                'Mensaje',
                'No ha eliminado este empleado',
                'warning'
            )
        }
    });
}