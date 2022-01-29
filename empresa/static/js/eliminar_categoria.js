function eliminarCategoria(id, nombre) {
    alert('Id de categoría: ' + id);

    Swal.fire({
        title: 'Mensaje de Salesemp',
        text: "¿Desea eliminar la categoría " + nombre + "?",
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
                'Categoría ' + nombre + ' eliminada correctamente',
                'success'
            );
        } else {
            Swal.fire(
                'Mensaje',
                'No has eliminado la categoría ' + nombre,
                'warning'
            );
        }
    });
}