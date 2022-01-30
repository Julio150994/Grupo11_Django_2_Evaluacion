function eliminar(id) {
    Swal.fire({
        title: 'Mensaje de Salesemp',
        text: '¿Desea eliminar esta categoría?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#076BCA',
        cancelButtonColor: '#C62D00',
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((categoria) => {
        if (categoria.isConfirmed) {
            window.location = '/eliminar_categoria/' + id;
        } else {
            window.location = '/categorias';
        }
    });
}