# MANUAL DE USUARIO
## Sistema de Gestión de Taller Mecánico

---

### **PORTADA**

**Sistema:** Gestión de Taller Mecánico  
**Integrantes del Equipo:**  
- Juan Pablo Maldonado Huenulef
- Maximiliano Javier Beltrán Barrueto
- Marcos Ignacio Villarroel Solís
- Benjamín Manuel Ignacio Moreira Arias

**Fecha:** Diciembre 2025

---

## 1. INTRODUCCIÓN

El Sistema de Gestión de Taller Mecánico es una aplicación web diseñada para facilitar la administración completa de un taller automotriz. Permite gestionar de manera eficiente la información de clientes, vehículos, servicios realizados y cotizaciones, centralizando toda la operación del taller en un solo lugar. El sistema incluye validaciones automáticas, generación de documentos PDF y gestión de archivos adjuntos.

---

## 2. MÓDULO DE CLIENTES

### ¿Qué es un cliente en el sistema?

Un cliente es la persona o empresa que solicita servicios en el taller. El sistema almacena su información de contacto para facilitar la comunicación y el seguimiento de los trabajos realizados en sus vehículos.

### Pasos para usar el módulo:

#### **2.1 Crear un nuevo cliente**

1. Hacer clic en **"Clientes"** en el menú lateral
2. Presionar el botón **"Nuevo Cliente"**
3. Completar el formulario:
   - **Nombre** (obligatorio): Nombre completo del cliente
   - RUT: Identificación fiscal (opcional)
   - Teléfono: Número de contacto (opcional)
   - Email: Correo electrónico (opcional)
   - Contacto: Persona de referencia (opcional)
   - Dirección: Ubicación física (opcional)
4. Hacer clic en **"Guardar"**

**Nota:** Solo el nombre es obligatorio. Los demás campos son opcionales pero recomendados para mantener información completa.

#### **2.2 Buscar un cliente**

1. En la lista de clientes, usar el cuadro de búsqueda superior
2. Escribir el nombre del cliente
3. El sistema filtrará automáticamente los resultados

#### **2.3 Editar un cliente**

1. Localizar al cliente en la lista
2. Hacer clic en el ícono de **editar** (lápiz)
3. Modificar los datos necesarios
4. Hacer clic en **"Guardar"**

#### **2.4 Desactivar un cliente**

1. Localizar al cliente en la lista
2. Hacer clic en el ícono de **eliminar** (papelera)
3. Confirmar la acción
4. El cliente se desactivará pero permanecerá en la base de datos

**Tip:** Los clientes desactivados pueden reactivarse desde "Clientes Inactivos" en el menú.

---

## 3. MÓDULO DE VEHÍCULOS

### ¿Qué es un vehículo en el sistema?

Un vehículo es el automóvil, camión o cualquier medio de transporte que pertenece a un cliente y requiere servicios de mantenimiento o reparación. Cada vehículo debe estar asociado a un cliente.

### Relación Cliente-Vehículo

Un cliente puede tener **múltiples vehículos**. El sistema mantiene un historial completo de todos los servicios realizados a cada vehículo.

### Pasos para usar el módulo:

#### **3.1 Registrar un nuevo vehículo**

1. Hacer clic en **"Vehículos"** en el menú lateral
2. Presionar el botón **"Nuevo Vehículo"**
3. Completar el formulario:
   - **Cliente** (obligatorio): Seleccionar el propietario
   - **Patente** (obligatoria): Identificador único del vehículo
   - Marca: Fabricante del vehículo (opcional)
   - Modelo: Línea del vehículo (opcional)
   - Año: Año de fabricación (opcional)
   - Chasis: Número de chasis (opcional)
   - Motor: Número de motor (opcional)
   - Kilometraje: Kilometraje actual (opcional)
4. Hacer clic en **"Guardar"**

**Si el cliente no existe:**
- Hacer clic en **"+ Registrar un vehículo"** 
- Se abrirá una ventana emergente para crear el cliente primero
- Una vez creado, regresar y completar el registro del vehículo

#### **3.2 Buscar un vehículo**

Existen dos formas de buscar:

**Por Patente:**
1. Usar el cuadro de búsqueda superior
2. Escribir la patente del vehículo
3. El sistema mostrará coincidencias en tiempo real

**Por Cliente:**
1. Buscar el nombre del cliente en el cuadro de búsqueda
2. Se mostrarán todos los vehículos asociados a ese cliente

#### **3.3 Ver detalles de un vehículo**

1. Hacer clic en la patente del vehículo en la lista
2. Se mostrará una vista detallada con:
   - Información del vehículo
   - Datos del propietario
   - Historial completo de servicios realizados

#### **3.4 Editar un vehículo**

1. Localizar el vehículo en la lista
2. Hacer clic en el ícono de **editar**
3. Modificar los datos necesarios
4. Hacer clic en **"Guardar"**

---

## 4. MÓDULO DE SERVICIOS

### ¿Qué es un servicio en el sistema?

Un servicio (u orden de trabajo) es el registro de un trabajo realizado o por realizar en un vehículo. Incluye la descripción del trabajo, fecha, estado y puede tener documentos y fotos adjuntas.

### Pasos para usar el módulo:

#### **4.1 Crear un nuevo servicio**

1. Hacer clic en **"Servicios"** en el menú lateral
2. Presionar el botón **"Nuevo Servicio"**
3. Completar el formulario:
   - **Vehículo** (obligatorio): Seleccionar de la lista
   - **Descripción del trabajo** (obligatorio): Detallar el trabajo a realizar
   - **Fecha del servicio** (obligatorio): Fecha de entrada/realización
   - Estado: Pendiente, En Proceso, Completado o Cancelado
4. Hacer clic en **"Registrar"**

**Validaciones automáticas:**
- No se puede guardar sin seleccionar un vehículo
- La descripción del trabajo es obligatoria
- Solo se muestran vehículos activos

#### **4.2 Cambiar el estado de un servicio**

1. Localizar el servicio en la lista
2. Hacer clic en el desplegable de **Estado**
3. Seleccionar el nuevo estado:
   - **Pendiente**: Trabajo aún no iniciado
   - **En Proceso**: Trabajo en progreso
   - **Completado**: Trabajo finalizado
   - **Cancelado**: Servicio cancelado
4. El cambio se guarda automáticamente

#### **4.3 Ver detalles y adjuntar documentos**

1. Hacer clic en el ícono de **documentos** del servicio
2. Se mostrará la vista de detalles con tres secciones:
   - Información del servicio
   - Documentos adjuntos
   - Cotizaciones asociadas

**Para subir un documento:**
1. En la sección "Documentos", completar:
   - **Tipo**: Factura, Boleta, Certificado, Presupuesto, Informe u Otro
   - **Fecha**: Fecha del documento
   - **Monto**: Valor del documento (debe ser mayor a cero)
   - **Archivo**: Seleccionar archivo PDF, Word, Excel o texto (máximo 10 MB)
2. Hacer clic en **"Subir"**
3. El documento aparecerá en la lista con opción de ver o eliminar

**Tip:** El total del servicio se actualiza automáticamente al sumar los montos de documentos y cotizaciones aprobadas.

#### **4.4 Agregar fotos del servicio**

1. Desde la vista de detalles, hacer clic en la pestaña **"Fotos del Servicio"**
2. Hacer clic en **"Seleccionar archivos"**
3. Elegir una o varias imágenes (JPG, PNG, GIF, WebP - máximo 5 MB cada una)
4. (Opcional) Agregar una descripción: "Estado del motor", "Daños en carrocería", etc.
5. Hacer clic en **"Subir"**
6. Las fotos se optimizan automáticamente y se muestran en la galería

**Funciones disponibles:**
- Hacer clic en una foto para verla en tamaño completo
- Eliminar fotos desde el ícono de papelera

#### **4.5 Editar un servicio**

1. Localizar el servicio en la lista
2. Hacer clic en el ícono de **editar**
3. Modificar los datos necesarios
4. Hacer clic en **"Guardar"**

#### **4.6 Eliminar un servicio**

1. Localizar el servicio en la lista
2. Hacer clic en el ícono de **eliminar**
3. Confirmar la acción en la ventana emergente
4. El servicio se eliminará permanentemente junto con sus documentos y fotos

---

## 5. MÓDULO DE COTIZACIONES

### ¿Qué es una cotización en el sistema?

Una cotización es un presupuesto formal que se genera para un cliente, detallando los servicios y/o productos a entregar, sus precios, y el total a pagar. Incluye información de la empresa, términos de pago y puede generarse como documento PDF.

### Pasos para usar el módulo:

#### **5.1 Crear una nueva cotización**

Existen dos formas de crear una cotización:

**Opción A: Desde un servicio existente**
1. Ir a **Servicios** → Hacer clic en **Documentos** del servicio
2. En la sección de cotizaciones, hacer clic en **"Nueva Cotización"**
3. El sistema precargará automáticamente:
   - Cliente asociado al vehículo
   - Referencia al servicio
4. Continuar con el paso 5.1.2

**Opción B: Crear cotización independiente**
1. Hacer clic en **"Cotizaciones"** en el menú lateral
2. Presionar el botón **"Nueva Cotización"**
3. Continuar con el paso 5.1.2

#### **5.1.2 Completar información de la cotización**

**Datos de la empresa (parte superior):**
- Nombre de la empresa
- RUT, Giro, Dirección, Teléfono, Email
- Número de cotización (se genera automáticamente)
- Fecha de emisión y fecha de validez

**Datos del cliente:**
- Seleccionar cliente o ingresar datos manualmente
- RUT, contacto, dirección, email

**Agregar ítems:**
1. El sistema crea automáticamente una categoría (ejemplo: "Servicios")
2. Para cada ítem, completar:
   - **Descripción**: Detalle del producto o servicio
   - **Cantidad**: Número de unidades
   - **Precio Unitario**: Precio por unidad
   - El **Total** se calcula automáticamente (Cantidad × Precio Unit.)
3. Hacer clic en **"+ Agregar Ítem"** para agregar más líneas
4. Hacer clic en **"+ Agregar Nueva Categoría"** para crear secciones (ej: "Repuestos", "Mano de Obra")

**Para eliminar ítems o categorías:**
- Hacer clic en el ícono de papelera (🗑)
- El sistema pide confirmación antes de eliminar

#### **5.2 Configurar términos y condiciones**

En la parte inferior del formulario:

1. **Forma de Pago**: Seleccionar entre:
   - Transferencia Bancaria
   - Efectivo
   - Cheque
   - Tarjeta

2. **Plazo de Pago**: Seleccionar entre:
   - Al Contado
   - 15, 30, 45, 60 o 90 días

3. **Notas Adicionales** (opcional):
   - Agregar condiciones especiales, garantías, o información relevante

#### **5.3 Ver totales automáticos**

El sistema calcula automáticamente:
- **Subtotal**: Suma de todos los ítems
- **IVA (19%)**: Impuesto sobre el subtotal
- **Total**: Subtotal + IVA

Los totales se actualizan en tiempo real mientras se agregan o modifican ítems.

#### **5.4 Guardar la cotización**

1. Revisar todos los datos
2. Hacer clic en **"Guardar Cotización"**
3. El sistema validará que todos los campos obligatorios estén completos
4. Si hay errores, se mostrarán en rojo indicando qué corregir
5. Una vez guardada, se redirige a la lista de cotizaciones

#### **5.5 Cambiar estado de una cotización**

Las cotizaciones pueden tener tres estados:

- **PENDIENTE**: Esperando respuesta del cliente
- **APROBADA**: Cliente aceptó la cotización
- **RECHAZADA**: Cliente no aceptó la cotización

**Para cambiar el estado:**
1. En la lista de cotizaciones, localizar la cotización
2. Hacer clic en el menú desplegable de **Estado**
3. Seleccionar el nuevo estado
4. El cambio se guarda automáticamente

**Importante:** Solo las cotizaciones **APROBADAS** se suman al total del servicio asociado.

#### **5.6 Generar PDF de la cotización**

1. En la lista de cotizaciones, localizar la cotización deseada
2. Hacer clic en el ícono de **PDF** (📄)
3. El sistema generará automáticamente un documento PDF profesional con:
   - Logo y datos de la empresa
   - Información del cliente
   - Desglose de ítems por categoría
   - Subtotal, IVA y Total
   - Términos de pago y notas

4. El PDF se abrirá en una nueva pestaña
5. Desde ahí puede:
   - Imprimirlo
   - Descargarlo
   - Enviarlo por correo

#### **5.7 Enviar cotización por correo electrónico**

1. En la lista de cotizaciones, hacer clic en el ícono de **correo** (✉️)
2. El sistema enviará automáticamente:
   - El PDF de la cotización adjunto
   - Un mensaje predeterminado
   - Al email del cliente registrado
3. Aparecerá un mensaje de confirmación cuando se envíe exitosamente

**Requisitos:**
- El cliente debe tener un email registrado
- El servidor de correo debe estar configurado

#### **5.8 Editar una cotización**

1. Localizar la cotización en la lista
2. Hacer clic en el ícono de **editar** (✏️)
3. Modificar los datos, ítems o términos necesarios
4. Hacer clic en **"Guardar Cotización"**

**Nota:** Si la cotización está asociada a un servicio, la relación se mantiene automáticamente.

#### **5.9 Duplicar una cotización**

Útil para crear presupuestos similares:

1. Localizar la cotización a duplicar
2. Hacer clic en el ícono de **duplicar** (📋)
3. El sistema creará una copia con:
   - Los mismos datos de empresa y cliente
   - Los mismos ítems
   - Nuevo número de cotización
   - Estado: PENDIENTE
   - Fechas actualizadas
4. Editar los datos necesarios
5. Guardar

#### **5.10 Eliminar una cotización**

1. Localizar la cotización en la lista
2. Hacer clic en el ícono de **eliminar** (🗑)
3. Confirmar la acción
4. La cotización se eliminará permanentemente

**Importante:** Si la cotización estaba APROBADA y asociada a un servicio, el total del servicio se recalculará automáticamente.

---

## 6. CONSEJOS DE USO

### Recomendaciones generales:

1. **Guardar antes de cambiar de página**
   - Siempre hacer clic en "Guardar" antes de salir de un formulario
   - El sistema no guarda cambios automáticamente

2. **Usar los buscadores**
   - Aprovechar las búsquedas por texto en clientes
   - Buscar vehículos por patente o nombre de cliente
   - Los resultados se filtran en tiempo real

3. **Verificar datos antes de generar PDF**
   - Revisar toda la información de la cotización
   - Confirmar que los montos sean correctos
   - Verificar email del cliente antes de enviar

4. **Mantener información actualizada**
   - Actualizar datos de contacto de clientes
   - Registrar el kilometraje actual de los vehículos
   - Cambiar estados de servicios según avance el trabajo

5. **Aprovechar las validaciones**
   - El sistema marca en rojo los campos obligatorios
   - Lee los mensajes de error para saber qué corregir
   - No intentes subir archivos muy grandes (máx. 10 MB documentos, 5 MB fotos)

6. **Gestionar archivos adjuntos**
   - Usa nombres descriptivos para los archivos antes de subirlos
   - Agrega descripciones a las fotos para identificarlas fácilmente
   - Formatos permitidos:
     - Documentos: PDF, Word, Excel, TXT
     - Fotos: JPG, PNG, GIF, WebP

7. **Backup de información**
   - Descarga regularmente los PDFs de cotizaciones importantes
   - Mantén respaldo de documentos críticos fuera del sistema

### Errores comunes y soluciones:

| Problema | Solución |
|----------|----------|
| "Este campo es obligatorio" | Completar todos los campos marcados con asterisco (*) |
| "El monto debe ser mayor a cero" | Ingresar un valor positivo en el campo monto |
| "Solo se permiten archivos PDF..." | Verificar que el archivo tenga la extensión correcta |
| "El archivo no debe superar los X MB" | Comprimir o reducir el tamaño del archivo |
| No puedo guardar el formulario | Revisar si hay campos en rojo con errores |
| La cotización no se asocia al servicio | Crearla desde la vista de documentos del servicio |

---

## 7. CONTACTO Y SOPORTE

### Información del equipo:

**Sistema:** Gestión de Taller Mecánico  
**Versión:** 1.0  
**Fecha de creación:** Diciembre 2025

**Soporte técnico:**  
Email: soporte.tallermec@gmail.com  
Teléfono: +56 9 8765 4321

**Desarrollado por:**
- Juan Pablo Maldonado Huenulef
- Maximiliano Javier Beltrán Barrueto
- Marcos Ignacio Villarroel Solís
- Benjamín Manuel Ignacio Moreira Arias

---

### Notas finales:

- Este sistema fue desarrollado como proyecto académico
- Para reportar problemas o sugerencias, contactar al equipo de desarrollo
- Se recomienda usar navegadores actualizados (Chrome, Firefox, Edge)
- Compatible con dispositivos móviles y tablets

---

**© 2025 - Sistema de Gestión de Taller Mecánico**  
*Todos los derechos reservados*
