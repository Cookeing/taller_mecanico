// static/js/rut-validation.js

function validarRut(input) {
    const rut = input.value.trim();
    
    if (!rut) {
        // Si está vacío, quitar clases de error
        input.classList.remove('is-invalid');
        input.classList.remove('is-valid');
        return true;
    }
    
    // Limpiar y formatear RUT
    const rutLimpio = rut.replace(/[^0-9kK-]/g, '');
    const rutFormateado = formatearRUT(rutLimpio);
    
    if (rutFormateado !== rut) {
        input.value = rutFormateado;
    }
    
    // Validar formato y dígito verificador
    if (validarFormatoRUT(rutFormateado) && validarDigitoVerificador(rutFormateado)) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        return true;
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        mostrarErrorRUT(input);
        return false;
    }
}

function formatearRUT(rut) {
    // Remover cualquier formato existente
    let rutLimpio = rut.replace(/[^0-9kK]/g, '');
    
    if (rutLimpio.length < 2) return rut;
    
    // Separar número y dígito verificador
    const dv = rutLimpio.slice(-1).toUpperCase();
    let numero = rutLimpio.slice(0, -1);
    
    // Formatear número con puntos
    numero = numero.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    
    return numero + '-' + dv;
}

function validarFormatoRUT(rut) {
    const patron = /^[0-9]{1,2}(?:\.[0-9]{3}){1,2}-[0-9kK]$/;
    return patron.test(rut);
}

function validarDigitoVerificador(rut) {
    const [numero, dv] = rut.split('-');
    const numeroLimpio = numero.replace(/\./g, '');
    
    let suma = 0;
    let multiplo = 2;
    
    // Recorrer el número de derecha a izquierda
    for (let i = numeroLimpio.length - 1; i >= 0; i--) {
        suma += parseInt(numeroLimpio.charAt(i)) * multiplo;
        multiplo = multiplo === 7 ? 2 : multiplo + 1;
    }
    
    const resto = 11 - (suma % 11);
    let dvCalculado = resto === 11 ? '0' : resto === 10 ? 'K' : resto.toString();
    
    return dvCalculado === dv.toUpperCase();
}

function mostrarErrorRUT(input) {
    // Remover mensajes de error existentes
    const existingError = input.parentNode.querySelector('.rut-error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Crear mensaje de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-danger small mt-1 rut-error-message';
    errorDiv.textContent = 'RUT inválido. Formato: 12.345.678-9';
    
    input.parentNode.appendChild(errorDiv);
}

// Validación en tiempo real mientras se escribe
document.addEventListener('DOMContentLoaded', function() {
    const rutInputs = document.querySelectorAll('input[name="rut"]');
    
    rutInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Formatear mientras se escribe
            const rut = this.value;
            const rutLimpio = rut.replace(/[^0-9kK-]/g, '');
            
            if (rutLimpio.length > 1) {
                const rutFormateado = formatearRUT(rutLimpio);
                if (rutFormateado !== rut) {
                    this.value = rutFormateado;
                }
            }
        });
        
        input.addEventListener('blur', function() {
            validarRut(this);
        });
    });
    
    // Validar RUT antes de enviar el formulario
    const form = document.getElementById('cliente-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const rutInput = this.querySelector('input[name="rut"]');
            if (rutInput && rutInput.value && !validarRut(rutInput)) {
                event.preventDefault();
                rutInput.focus();
            }
        });
    }
});