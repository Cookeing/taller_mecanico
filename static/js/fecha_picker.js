document.addEventListener('DOMContentLoaded', function () {
  try {
    var el = document.getElementById('id_fecha_servicio');
    if (!el) return;

    // Inicializa flatpickr con formato día-mes-año
    var fp = flatpickr(el, {
      dateFormat: 'd-m-Y',
      altInput: false,
      // Seguridad estricta: no permitir entrada manual, obligar a usar el picker
      allowInput: false,
      clickOpens: true,
      // locale puede ajustarse si se carga el paquete de idioma
    });

    // Añadir un ícono de calendario como background (SVG inline)
    var svg = encodeURIComponent(
      "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='4' width='18' height='18' rx='2' ry='2'></rect><line x1='16' y1='2' x2='16' y2='6'></line><line x1='8' y1='2' x2='8' y2='6'></line><line x1='3' y1='10' x2='21' y2='10'></line></svg>"
    );
    el.style.backgroundImage = "url('data:image/svg+xml;utf8," + svg + "')";
    el.style.backgroundRepeat = 'no-repeat';
    el.style.backgroundPosition = 'right 10px center';
    el.style.backgroundSize = '18px 18px';
    el.style.paddingRight = '36px';
    el.style.cursor = 'text';

    // Si el usuario hace click cerca del borde derecho (donde está el icono), abrir el calendario
    el.addEventListener('click', function (e) {
      var rect = el.getBoundingClientRect();
      // si el click ocurrió en los 40px derechos, abrir
      if (e.clientX > rect.right - 40) {
        if (fp) fp.open();
      }
    });

    // Si existe un botón junto al input para abrir el calendario, enlazarlo
    var btn = document.getElementById('btn_fecha_servicio');
    if (btn) {
      btn.addEventListener('click', function (ev) {
        ev.preventDefault();
        if (fp) fp.open();
        // enfocar el input para accesibilidad
        el.focus();
      });
    }

    // Con allowInput: false y el input marcado readonly, no necesitamos máscara JS.
    // flatpickr gestionará la entrada y la formateará a 'd-m-Y'.
  } catch (err) {
    // no bloquear si flatpickr no está disponible
    console.warn('fecha_picker init error:', err);
  }
});
