# PRESENTACIÓN POWERPOINT
## Sistema de Gestión de Taller Mecánico

---

## SLIDE 1: PORTADA

**Título principal:**
SISTEMA DE GESTIÓN DE TALLER MECÁNICO

**Subtítulo:**
Proyecto de Desarrollo de Software

**Integrantes:**
- Juan Pablo Maldonado Huenulef
- Maximiliano Javier Beltrán Barrueto
- Marcos Ignacio Villarroel Solís
- Benjamín Manuel Ignacio Moreira Arias

**Fecha:** Diciembre 2025

---

## SLIDE 2: INTRODUCCIÓN

**Título:** ¿Qué es el sistema?

**Contenido:**
El Sistema de Gestión de Taller Mecánico es una aplicación web que permite:

- Gestionar clientes y sus datos de contacto
- Registrar vehículos y su historial de servicios
- Crear órdenes de trabajo y servicio
- Generar cotizaciones profesionales con PDF
- Adjuntar documentos y fotos a los servicios
- Enviar cotizaciones por correo electrónico

**Objetivo:**
Centralizar y automatizar todas las operaciones administrativas de un taller automotriz.

---

## SLIDE 3: PROBLEMA QUE RESUELVE

**Título:** Problemática

**Antes del sistema:**
- Registros en papel o Excel desorganizados
- Pérdida de información de clientes
- Cotizaciones hechas manualmente
- No hay historial de servicios por vehículo
- Dificultad para hacer seguimiento de trabajos

**Con nuestro sistema:**
- Información centralizada y segura
- Búsquedas rápidas por cliente o patente
- Cotizaciones automáticas con cálculo de IVA
- Historial completo por vehículo
- Seguimiento de estados de servicios y cotizaciones

---

## SLIDE 4: TECNOLOGÍAS UTILIZADAS

**Título:** Stack Tecnológico

**Backend:**
- Python 3.13.0
- Django 4.2.25
- Django REST Framework (si aplica)

**Frontend:**
- Bootstrap 5.3.2
- JavaScript (ES6+)
- CSS3 con sistema de temas (claro/oscuro)

**Base de Datos:**
- MySQL 8.0

**Herramientas:**
- Git / GitHub
- Visual Studio Code
- Pillow (optimización de imágenes)

---

## SLIDE 5: ARQUITECTURA DEL SISTEMA

**Título:** Arquitectura y Módulos

**Diagrama conceptual:**
```
┌─────────────────────────────────────┐
│         INTERFAZ WEB                │
│      (Bootstrap + JavaScript)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       DJANGO FRAMEWORK              │
│  ┌───────────────────────────────┐  │
│  │  Módulo Clientes              │  │
│  │  Módulo Vehículos             │  │
│  │  Módulo Servicios             │  │
│  │  Módulo Cotizaciones          │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       BASE DE DATOS MySQL           │
└─────────────────────────────────────┘
```

**Patrón:** Modelo-Vista-Template (MVT) de Django

---

## SLIDE 6: MÓDULO DE CLIENTES

**Título:** Gestión de Clientes

**Funcionalidades:**
- Registro de clientes con validación de RUT
- Búsqueda en tiempo real por nombre
- Edición de datos de contacto
- Eliminación lógica (soft delete)
- Reactivación de clientes inactivos
- Listado con paginación

**Campos:**
- Nombre, RUT, Teléfono, Email, Contacto, Dirección

**Validación:**
- Solo el nombre es obligatorio (facilita el registro rápido)

---

## SLIDE 7: MÓDULO DE VEHÍCULOS

**Título:** Gestión de Vehículos

**Funcionalidades:**
- Registro de vehículos asociados a clientes
- Búsqueda por patente o cliente
- Validación de patentes únicas
- Historial completo de servicios
- Vista detallada por vehículo
- Eliminación lógica

**Campos:**
- Cliente, Patente, Marca, Modelo, Año, Chasis, Motor, Kilometraje

**Relación:**
- Un cliente puede tener múltiples vehículos
- Cada vehículo pertenece a un solo cliente

---

## SLIDE 8: MÓDULO DE SERVICIOS

**Título:** Órdenes de Trabajo

**Funcionalidades:**
- Crear servicios para vehículos específicos
- Cambio de estados: Pendiente, En Proceso, Completado, Cancelado
- Adjuntar documentos (PDF, Word, Excel - máx. 10 MB)
- Adjuntar fotos con optimización automática (máx. 5 MB c/u)
- Cálculo automático del total del servicio
- Asociación con cotizaciones

**Estados del servicio:**
- Pendiente → En Proceso → Completado
- Cancelado (en cualquier momento)

**Documentos:**
- Tipos: Factura, Boleta, Certificado, Presupuesto, Informe, Otro

---

## SLIDE 9: MÓDULO DE COTIZACIONES (1/2)

**Título:** Generación de Cotizaciones

**Características principales:**
- Creación desde servicio o independiente
- Organización por categorías de ítems
- Cálculo automático de subtotal, IVA (19%) y total
- Estados: Pendiente, Aprobada, Rechazada
- Términos de pago configurables
- Numeración automática

**Datos de empresa personalizables:**
- Nombre, RUT, Giro, Dirección, Teléfono, Email

**Datos del cliente:**
- Precargados desde el servicio asociado

---

## SLIDE 10: MÓDULO DE COTIZACIONES (2/2)

**Título:** Gestión de Cotizaciones

**Funcionalidades avanzadas:**
- Generación de PDF profesional
- Envío por correo electrónico
- Duplicación de cotizaciones
- Edición después de creada
- Eliminación con recalculación automática

**Ítems personalizables:**
- Descripción, Cantidad, Precio Unitario
- Total por ítem automático
- Múltiples categorías (ej: Mano de Obra, Repuestos)

**Términos:**
- Forma de pago: Transferencia, Efectivo, Cheque, Tarjeta
- Plazo: Al contado, 15, 30, 45, 60, 90 días

---

## SLIDE 11: CARACTERÍSTICAS DESTACADAS

**Título:** Funcionalidades Especiales

**Interfaz de usuario:**
- Diseño responsive (funciona en móviles y tablets)
- Tema claro y oscuro
- Menú lateral colapsable
- Búsquedas en tiempo real

**Validaciones:**
- Formularios con validación frontend y backend
- Mensajes de error descriptivos
- Campos obligatorios marcados visualmente
- Validación de tipos de archivo y tamaño

**Automatizaciones:**
- Cálculos matemáticos automáticos
- Numeración de cotizaciones
- Optimización de imágenes
- Actualización de totales en tiempo real

---

## SLIDE 12: FLUJO DE TRABAJO

**Título:** Flujo Típico de Uso

**Paso a paso:**

1. **Registrar Cliente**
   - Ingresar datos básicos del cliente

2. **Registrar Vehículo**
   - Asociar vehículo al cliente

3. **Crear Servicio**
   - Describir trabajo a realizar
   - Cambiar estado según avance

4. **Adjuntar Documentos/Fotos**
   - Evidencia del trabajo realizado

5. **Generar Cotización**
   - Agregar ítems y precios
   - Calcular totales

6. **Generar PDF y Enviar**
   - Documento profesional para el cliente

---

## SLIDE 13: DEMOSTRACIÓN EN VIVO

**Título:** Demo del Sistema

**Lo que vamos a mostrar:**

1. Crear un cliente nuevo
2. Registrar su vehículo
3. Generar una orden de servicio
4. Crear cotización con múltiples ítems
5. Generar PDF profesional
6. Cambiar estado de cotización

**Tiempo estimado:** 8-10 minutos

---

## SLIDE 14: PRUEBAS REALIZADAS

**Título:** Validación del Sistema

**Tipos de pruebas:**
- Pruebas funcionales por módulo
- Pruebas de integración (flujo completo)
- Pruebas de validación de formularios
- Pruebas de generación de PDF
- Pruebas de carga de archivos

**Resultados:**
- Todos los casos de prueba principales: OK
- Validaciones funcionando correctamente
- Cálculos automáticos verificados
- Generación de PDF exitosa

**Responsable:** Persona 1 - Pruebas

---

## SLIDE 15: INSTALACIÓN Y DESPLIEGUE

**Título:** Cómo Instalar el Sistema

**Requisitos:**
- Python 3.13+
- MySQL 8.0
- Navegador web moderno

**Pasos:**
1. Clonar repositorio
2. Crear entorno virtual
3. Instalar dependencias (`pip install -r requirements.txt`)
4. Configurar base de datos
5. Ejecutar migraciones (`python manage.py migrate`)
6. Crear superusuario
7. Ejecutar servidor (`python manage.py runserver`)

**Responsable:** Persona 2 - Instalación y entorno

---

## SLIDE 16: MANTENCIÓN Y FUTURO

**Título:** Plan de Mantención

**Mantención Correctiva:**
- Corrección de bugs detectados

**Mantención Preventiva:**
- Actualización de dependencias
- Backups periódicos de base de datos

**Mantención Adaptativa:**
- Nuevos campos o módulos según necesidades

**Mantención Perfectiva:**
- Mejoras de rendimiento
- Optimización de interfaz

**Responsable:** Persona 4 - Mantención y cambios futuros

---

## SLIDE 17: CAMBIOS FUTUROS

**Título:** Próximas Funcionalidades

**Mejoras planificadas:**
- Dashboard con estadísticas y gráficos
- Reportes de servicios por período
- Sistema de inventario de repuestos
- Notificaciones automáticas por email/SMS
- App móvil nativa
- Integración con sistemas de pago online
- Recordatorios de mantención preventiva
- Sistema de citas online

**Proceso de gestión de cambios:**
- Recepción de solicitudes
- Evaluación de prioridad
- Planificación en backlog
- Desarrollo e implementación
- Pruebas y validación

---

## SLIDE 18: EQUIPO Y RESPONSABILIDADES

**Título:** Distribución del Trabajo

**Juan Pablo Maldonado Huenulef**
- Rol: Pruebas y validación
- Responsabilidad: Casos de prueba e integración

**Maximiliano Javier Beltrán Barrueto**
- Rol: Instalación y entorno
- Responsabilidad: Manual de instalación y configuración

**Marcos Ignacio Villarroel Solís**
- Rol: Documentación
- Responsabilidad: Manual de usuario y guion de demo

**Benjamín Manuel Ignacio Moreira Arias**
- Rol: Mantención y coordinación
- Responsabilidad: Protocolo de mantención y gestión futura

---

## SLIDE 19: LECCIONES APRENDIDAS

**Título:** Aprendizajes del Proyecto

**Técnicos:**
- Implementación de patrón MVT con Django
- Gestión de relaciones en base de datos
- Validaciones frontend y backend
- Generación dinámica de PDFs
- Optimización de archivos multimedia

**Metodológicos:**
- Trabajo en equipo distribuido
- Gestión de tareas por historias de usuario
- Importancia de la documentación
- Pruebas continuas durante desarrollo

**Profesionales:**
- Comunicación efectiva en equipo
- Cumplimiento de plazos
- Adaptación a cambios de requisitos

---

## SLIDE 20: CONCLUSIONES

**Título:** Conclusiones

**Logros alcanzados:**
- Sistema funcional y completo según requerimientos
- Interfaz intuitiva y profesional
- Documentación exhaustiva
- Código limpio y mantenible
- Pruebas exitosas de todos los módulos

**Valor del proyecto:**
- Solución real a problema de talleres mecánicos
- Automatización de procesos administrativos
- Mejora en la gestión de información
- Base sólida para futuras ampliaciones

**Cumplimiento:**
- Todos los criterios de la rúbrica cumplidos
- Sistema listo para uso en producción

---

## SLIDE 21: PREGUNTAS

**Título:** ¿Preguntas?

**Contacto del equipo:**
Email: soporte.tallermec@gmail.com
Teléfono: +56 9 8765 4321

**Repositorio:**
GitHub: Cookeing/taller_mecanico

**Agradecimientos:**
Gracias por su atención.

---

## SLIDE 22: REFERENCIAS (OPCIONAL)

**Título:** Referencias y Recursos

**Documentación utilizada:**
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- Python Documentation: https://docs.python.org/

**Librerías principales:**
- Django 4.2.25
- Bootstrap 5.3.2
- Pillow (PIL) para imágenes
- WeasyPrint o ReportLab para PDFs

**Recursos de aprendizaje:**
- MDN Web Docs
- Stack Overflow
- Django Community

---

## NOTAS PARA CREAR LA PPT

### Diseño recomendado:
- **Colores:** Azul oscuro (#1a237e) y blanco para contraste profesional
- **Fuente:** Arial o Calibri (legible desde lejos)
- **Tamaño de texto:** Mínimo 24pt para contenido, 36pt para títulos
- **Imágenes:** Agregar capturas de pantalla del sistema en slides 6-11

### Capturas a incluir:
1. **Slide 6:** Listado de clientes
2. **Slide 7:** Detalle de vehículo con historial
3. **Slide 8:** Formulario de servicio con fotos
4. **Slide 10:** Cotización con PDF generado
5. **Slide 11:** Vista de tema claro y oscuro

### Animaciones (opcional):
- Entradas suaves para bullets (aparición gradual)
- No abusar de efectos (máximo 1-2 por slide)

### Tiempo por slide:
- Slides 1-5: 30-45 segundos cada uno
- Slides 6-11: 1 minuto cada uno (explicando módulos)
- Slide 13: DEMO (8-10 minutos)
- Slides 14-22: 30-45 segundos cada uno

**Tiempo total estimado:** 20-25 minutos (con demo incluida)

---

**Preparado por:** Persona 3  
**Versión:** 1.0  
**Fecha:** Diciembre 2025
