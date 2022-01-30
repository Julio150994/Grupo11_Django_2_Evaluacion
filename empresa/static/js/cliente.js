function eliminar(id) {
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
            window.location = '/eliminar_cliente/' + id;
        } else {
            window.location = '/clientes/';
        }
    });
}