const empleado = document.getElementById('id_emp');
const id = document.getElementById('id');
const btnEmpleado = document.querySelectorAll('.btnEmpleado');

(function() {
    empleado.addEventListener('submit', function(e) {
        let username_emp = String(id.value).trim();

        if (username_emp.length === 0) {
            alert("El usuario no puede ser nulo");
            e.preventDefault();
        }
    });

    btnEmpleado.forEach(button => {
        btnEmpleado.addEventListener('click', function(e) {
            let confirmEmpleado = confirm("¿Desea eliminar este empleado?");

            if (!confirmEmpleado) {
                alert("El empleado no se pudo eliminar");
                e.preventDefault();
            } else {
                alert("El empleado se pudo eliminar correctamente");
            }
        })
        console.log(button);
    });
})();