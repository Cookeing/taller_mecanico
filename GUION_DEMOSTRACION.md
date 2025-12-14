# GUION DE DEMOSTRACIÓN
## Sistema de Gestión de Taller Mecánico

---

## INFORMACIÓN DE LA PRESENTACIÓN

**Duración estimada:** 8-10 minutos  
**Presentador:** [Nombre de quien hará la demo]  
**Flujo a demostrar:** Cliente → Vehículo → Servicio → Cotización → PDF

---

## 1. INTRODUCCIÓN (1 minuto)

### Saludo inicial
"Buenos días/tardes. Somos el equipo conformado por Juan Pablo Maldonado, Maximiliano Beltrán, Marcos Villarroel y Benjamín Moreira."

### Presentación del sistema
"Hoy presentamos el **Sistema de Gestión de Taller Mecánico**, una aplicación web desarrollada en Django que permite administrar de forma integral todas las operaciones de un taller automotriz."

### Objetivo de la demo
"En esta demostración mostraremos el flujo completo del sistema: desde el registro de un cliente hasta la generación y envío de una cotización en formato PDF."

---

## 2. EXPLICACIÓN DEL FLUJO (30 segundos)

"El flujo que vamos a demostrar es el siguiente:

1. **Registrar un cliente nuevo** en el sistema
2. **Crear un vehículo** asociado a ese cliente
3. **Generar una orden de servicio** para ese vehículo
4. **Crear una cotización** con ítems y precios
5. **Generar el PDF** y mostrar el envío por correo

Este flujo representa el caso de uso más común en un taller mecánico real."

---

## 3. DEMOSTRACIÓN PASO A PASO (6-7 minutos)

### PASO 1: Registrar un Cliente (1 minuto)

**Qué decir mientras navegas:**
"Primero, accedemos al módulo de **Clientes** desde el menú lateral."

**Acciones:**
- Hacer clic en "Clientes"
- Hacer clic en "Nuevo Cliente"

**Qué decir mientras completas el formulario:**
"El sistema nos solicita los datos del cliente. Vamos a registrar a **Juan Pérez**."

**Datos a ingresar:**
- Nombre: Juan Pérez
- RUT: 12.345.678-9
- Teléfono: +56 9 8888 7777
- Email: juan.perez@email.com
- Dirección: Av. Principal 123, Santiago

**Qué decir al guardar:**
"Hacemos clic en **Guardar** y el sistema valida la información. Como pueden ver, el cliente se agregó exitosamente a la lista."

**Mostrar:**
- Cliente aparece en el listado
- Resaltar la búsqueda en tiempo real si escribes "Juan"

---

### PASO 2: Registrar un Vehículo (1 minuto)

**Qué decir mientras navegas:**
"Ahora vamos al módulo de **Vehículos** para registrar el auto de Juan Pérez."

**Acciones:**
- Hacer clic en "Vehículos"
- Hacer clic en "Nuevo Vehículo"

**Qué decir mientras completas el formulario:**
"Seleccionamos al cliente **Juan Pérez** y completamos los datos del vehículo."

**Datos a ingresar:**
- Cliente: Juan Pérez (seleccionar del dropdown)
- Patente: BBCC22
- Marca: Toyota
- Modelo: Corolla
- Año: 2018
- Kilometraje: 85000

**Qué decir al guardar:**
"El sistema valida que la patente sea única y registra el vehículo. Ahora podemos ver el vehículo en la lista con su propietario."

**Mostrar:**
- Vehículo aparece en el listado
- Hacer clic en la patente para ver detalles y el historial

---

### PASO 3: Crear una Orden de Servicio (1.5 minutos)

**Qué decir mientras navegas:**
"Con el cliente y vehículo registrados, ahora creamos una **Orden de Servicio** en el módulo de Servicios."

**Acciones:**
- Hacer clic en "Servicios"
- Hacer clic en "Nuevo Servicio"

**Qué decir mientras completas el formulario:**
"Seleccionamos el vehículo **BBCC22 - Toyota Corolla** y describimos el trabajo a realizar."

**Datos a ingresar:**
- Vehículo: BBCC22 - Juan Pérez
- Descripción: Cambio de aceite, filtros y revisión de frenos
- Fecha: (seleccionar fecha actual)
- Estado: En Proceso

**Qué decir al guardar:**
"Registramos el servicio y ahora podemos gestionarlo desde la lista."

**Acciones adicionales:**
- Hacer clic en el ícono de documentos del servicio recién creado

**Qué decir:**
"Desde aquí podemos ver los detalles del servicio, subir documentos, adjuntar fotos y crear cotizaciones. Vamos a crear una cotización para este servicio."

---

### PASO 4: Crear Cotización (2.5 minutos)

**Qué decir:**
"Ahora generaremos una cotización formal para el cliente con los trabajos y repuestos necesarios."

**Acciones:**
- Hacer clic en "Nueva Cotización" desde la vista de documentos del servicio

**Qué decir mientras completas:**
"El sistema precarga automáticamente los datos del cliente y la referencia al servicio."

**PARTE A: Datos de la empresa**
"Primero completamos los datos de nuestra empresa:"

- Empresa: Taller Mecánico Los Expertos
- RUT: 76.123.456-7
- Giro: Reparación y mantención automotriz
- Dirección: Av. Industrial 456, Santiago
- Teléfono: +56 2 2345 6789
- Email: contacto@tallerexpertos.cl

**PARTE B: Verificar datos del cliente**
"Los datos del cliente se cargaron automáticamente desde el servicio."

**PARTE C: Agregar ítems**
"Ahora agregamos los ítems de la cotización. El sistema permite organizarlos por categorías."

**Categoría 1: Mano de Obra**
- Ítem 1:
  - Descripción: Cambio de aceite y filtro
  - Cantidad: 1
  - Precio Unitario: 25000
  
- Hacer clic en "+ Agregar Ítem"
- Ítem 2:
  - Descripción: Revisión de frenos
  - Cantidad: 1
  - Precio Unitario: 15000

**Hacer clic en "+ Agregar Nueva Categoría"**

**Categoría 2: Repuestos**
- Ítem 1:
  - Descripción: Aceite sintético 5W-30 (4 litros)
  - Cantidad: 1
  - Precio Unitario: 32000
  
- Hacer clic en "+ Agregar Ítem"
- Ítem 2:
  - Descripción: Filtro de aceite
  - Cantidad: 1
  - Precio Unitario: 8000

**Qué decir mientras agregas ítems:**
"Como pueden observar, el sistema calcula automáticamente el total de cada ítem multiplicando cantidad por precio unitario."

**PARTE D: Términos de pago**
"Ahora configuramos los términos comerciales:"

- Forma de Pago: Transferencia Bancaria
- Plazo de Pago: 30 días
- Notas Adicionales: "Garantía de 3 meses en mano de obra. Repuestos con garantía del fabricante."

**Qué decir antes de guardar:**
"En la parte inferior, el sistema muestra el resumen financiero: **Subtotal, IVA del 19% y Total Final**. En este caso, el total es de **$95.200**."

**Acciones:**
- Hacer clic en "Guardar Cotización"

**Qué decir:**
"La cotización se ha guardado exitosamente y aparece en la lista con estado **PENDIENTE**."

---

### PASO 5: Generar PDF y Enviar (1 minuto)

**Qué decir:**
"Ahora vamos a generar el documento PDF de la cotización para enviarlo al cliente."

**Acciones:**
- En la lista de cotizaciones, hacer clic en el ícono de PDF

**Qué decir mientras se genera:**
"El sistema genera automáticamente un documento profesional con toda la información: datos de la empresa, del cliente, desglose de ítems por categoría, y los totales con IVA."

**Mostrar el PDF:**
- Hacer scroll por el documento
- Resaltar: logo, número de cotización, desglose, totales

**Qué decir:**
"Este PDF puede imprimirse o descargarse. Además, el sistema permite enviarlo directamente al correo del cliente."

**Acciones (opcional si funciona el envío):**
- Volver a la lista de cotizaciones
- Hacer clic en el ícono de correo
- Mostrar mensaje de confirmación de envío

**Si no funciona el envío por correo, decir:**
"El sistema incluye la funcionalidad de envío por correo electrónico, aunque para esta demo nos enfocaremos en la generación del PDF."

---

### PASO 6: Cambiar Estado de Cotización (30 segundos)

**Qué decir:**
"Finalmente, cuando el cliente aprueba la cotización, podemos cambiar su estado directamente desde el listado."

**Acciones:**
- Hacer clic en el desplegable de Estado
- Cambiar de "PENDIENTE" a "APROBADA"

**Qué decir:**
"Al aprobar la cotización, el sistema automáticamente actualiza el total del servicio asociado, sumando el monto de esta cotización."

**Mostrar (opcional):**
- Volver a la vista del servicio
- Mostrar que el total del servicio se actualizó

---

## 4. CIERRE DE LA DEMOSTRACIÓN (30 segundos)

### Resumen del flujo
"Con esto hemos demostrado el flujo completo del sistema:

1. Registramos un cliente nuevo
2. Agregamos su vehículo
3. Creamos una orden de servicio
4. Generamos una cotización profesional con cálculos automáticos
5. Obtuvimos un PDF listo para enviar al cliente

Este flujo cumple con todos los requerimientos funcionales definidos para el proyecto."

### Características destacadas
"Además, el sistema incluye:
- Validaciones automáticas de datos
- Búsquedas en tiempo real
- Cálculos automáticos de IVA y totales
- Gestión de documentos y fotos
- Sistema de estados para seguimiento
- Generación de reportes en PDF"

### Frase final
"Esto concluye nuestra demostración. Quedamos atentos a sus preguntas."

---

## 5. POSIBLES PREGUNTAS Y RESPUESTAS

### P1: "¿Qué pasa si elimino un cliente?"
**R:** "El sistema implementa eliminación lógica (soft delete). El cliente se desactiva pero permanece en la base de datos con sus relaciones intactas. Puede reactivarse desde el módulo de Clientes Inactivos."

### P2: "¿Cómo manejan la seguridad?"
**R:** "El sistema utiliza el sistema de autenticación de Django con contraseñas hasheadas, protección CSRF en formularios y validación de permisos por usuario."

### P3: "¿Qué pasa si dos vehículos tienen la misma patente?"
**R:** "El sistema valida que las patentes sean únicas a nivel de base de datos. No permite duplicados."

### P4: "¿Pueden modificar una cotización después de crearla?"
**R:** "Sí, las cotizaciones pueden editarse en cualquier momento. Si estaba aprobada y se elimina, el total del servicio se recalcula automáticamente."

### P5: "¿Cómo se calcula el total del servicio?"
**R:** "El total se calcula sumando los montos de todos los documentos adjuntos más las cotizaciones que estén en estado APROBADA."

### P6: "¿Qué tecnologías usaron?"
**R:** "Django 4.2.25 como framework backend, Python 3.13, MySQL como base de datos, Bootstrap 5 para el frontend con sistema de temas claro/oscuro."

### P7: "¿El sistema es responsive?"
**R:** "Sí, utilizamos Bootstrap que es mobile-first, por lo que funciona en tablets y móviles."

### P8: "¿Cómo gestionan las fotos para que no ocupen mucho espacio?"
**R:** "Las imágenes se optimizan automáticamente usando Pillow, reduciendo su calidad al 85% sin pérdida visual significativa."

---

## CONSEJOS PARA LA PRESENTACIÓN

### Antes de empezar:
1. Tener el servidor corriendo (`python manage.py runserver`)
2. Abrir el navegador con la aplicación ya cargada
3. Tener datos de prueba listos por si falla la conexión
4. Probar el flujo completo al menos 2 veces antes de presentar

### Durante la demo:
1. Hablar claro y a velocidad moderada
2. Explicar QUÉ haces y POR QUÉ es importante
3. No apresurarse si algo tarda en cargar
4. Si algo falla, mantener la calma y usar datos de ejemplo preparados

### Distribución de tiempo:
- Introducción: 1 min
- Cliente: 1 min
- Vehículo: 1 min
- Servicio: 1.5 min
- Cotización: 2.5 min
- PDF: 1 min
- Cierre: 0.5 min
- **Total: ~8-9 minutos**

### Frases útiles:
- "Como pueden observar..."
- "El sistema valida automáticamente..."
- "Esto cumple con el requisito de..."
- "Esto facilita al usuario porque..."

---

## DATOS DE PRUEBA DE RESPALDO

Por si algo falla durante la demo, tener estos datos preparados:

**Cliente alternativo:**
- Nombre: María González
- RUT: 15.678.234-K
- Teléfono: +56 9 7777 6666
- Email: maria.gonzalez@email.com

**Vehículo alternativo:**
- Patente: XYZA99
- Marca: Chevrolet
- Modelo: Spark
- Año: 2020

**Servicio alternativo:**
- Descripción: Alineación y balanceo de neumáticos

---

**Preparado por:** Persona 3 - Manual de usuario y demo  
**Fecha:** Diciembre 2025  
**Versión:** 1.0
