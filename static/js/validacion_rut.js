function formatearRUT(rut) {
    let rutLimpio = rut.replace(/[^0-9kK]/g, '');
    if (rutLimpio.length < 2) return rut;
    const dv = rutLimpio.slice(-1).toUpperCase();
    let numero = rutLimpio.slice(0, -1);
    numero = numero.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return numero + '-' + dv;
}

document.addEventListener('DOMContentLoaded', function() {
    const rutInputs = document.querySelectorAll('input[name="rut"]');
    rutInputs.forEach(input => {
        input.addEventListener('input', function() {
            const rut = this.value;
            const rutLimpio = rut.replace(/[^0-9kK-]/g, '');
            if (rutLimpio.length > 1) {
                const rutFormateado = formatearRUT(rutLimpio);
                if (rutFormateado !== rut) {
                    this.value = rutFormateado;
                }
            }
        });
    });
});
