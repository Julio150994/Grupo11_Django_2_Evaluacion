function eliminarCliente() {
    Swal.fire({
        title: 'Mensaje de Salesemp',
        text: "¿Desea eliminar este cliente?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#076BCA',
        cancelButtonColor: '#C62D00',
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((cliente) => {
        if (cliente.isConfirmed) {
            Swal.fire(
                'Mensaje',
                'Cliente eliminado correctamente',
                'success'
            );
        }
        else {
            Swal.fire(
                'Mensaje',
                'No ha eliminado este cliente',
                'warning'
            );
        }
    });
}