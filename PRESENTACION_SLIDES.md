---
title: "Sistema de Gestión de Taller Mecánico"
subtitle: "Proyecto de Desarrollo de Software"
author:
  - Juan Pablo Maldonado Huenulef
  - Maximiliano Javier Beltrán Barrueto
  - Marcos Ignacio Villarroel Solís
  - Benjamín Manuel Ignacio Moreira Arias
date: "Diciembre 2025"
---

# Introducción

## ¿Qué es el sistema?

El Sistema de Gestión de Taller Mecánico es una aplicación web que permite:

- Gestionar clientes y sus datos de contacto
- Registrar vehículos y su historial de servicios
- Crear órdenes de trabajo y servicio
- Generar cotizaciones profesionales con PDF
- Adjuntar documentos y fotos a los servicios
- Enviar cotizaciones por correo electrónico

**Objetivo:** Centralizar y automatizar todas las operaciones administrativas de un taller automotriz.

---

# Problemática

## Antes del sistema

- Registros en papel o Excel desorganizados
- Pérdida de información de clientes
- Cotizaciones hechas manualmente
- No hay historial de servicios por vehículo
- Dificultad para hacer seguimiento de trabajos

## Con nuestro sistema

- Información centralizada y segura
- Búsquedas rápidas por cliente o patente
- Cotizaciones automáticas con cálculo de IVA
- Historial completo por vehículo
- Seguimiento de estados de servicios y cotizaciones

---

# Tecnologías Utilizadas

## Stack Tecnológico

**Backend:**

- Python 3.13.0
- Django 4.2.25

**Frontend:**

- Bootstrap 5.3.2
- JavaScript (ES6+)
- CSS3 con sistema de temas

**Base de Datos:**

- MySQL 8.0

**Herramientas:**

- Git / GitHub
- Visual Studio Code
- Pillow (optimización de imágenes)

---

# Arquitectura del Sistema

## Arquitectura y Módulos

**Patrón:** Modelo-Vista-Template (MVT) de Django

**Módulos principales:**

- Módulo Clientes
- Módulo Vehículos
- Módulo Servicios
- Módulo Cotizaciones

**Flujo:**

Interfaz Web → Django Framework → Base de Datos MySQL

---

# Módulo de Clientes

## Gestión de Clientes

**Funcionalidades:**

- Registro con validación de RUT
- Búsqueda en tiempo real
- Edición de datos de contacto
- Eliminación lógica (soft delete)
- Reactivación de clientes inactivos

**Campos:**

- Nombre, RUT, Teléfono, Email, Contacto, Dirección

**Validación:**

- Solo el nombre es obligatorio

---

# Módulo de Vehículos

## Gestión de Vehículos

**Funcionalidades:**

- Registro asociado a clientes
- Búsqueda por patente o cliente
- Validación de patentes únicas
- Historial completo de servicios
- Vista detallada por vehículo

**Relación:**

- Un cliente puede tener múltiples vehículos
- Cada vehículo pertenece a un solo cliente

---

# Módulo de Servicios

## Órdenes de Trabajo

**Funcionalidades:**

- Crear servicios para vehículos específicos
- Estados: Pendiente, En Proceso, Completado, Cancelado
- Adjuntar documentos (PDF, Word, Excel - máx. 10 MB)
- Adjuntar fotos con optimización (máx. 5 MB c/u)
- Cálculo automático del total
- Asociación con cotizaciones

**Documentos:**

- Tipos: Factura, Boleta, Certificado, Presupuesto, Informe, Otro

---

# Módulo de Cotizaciones (1)

## Generación de Cotizaciones

**Características:**

- Creación desde servicio o independiente
- Organización por categorías de ítems
- Cálculo automático: Subtotal, IVA (19%), Total
- Estados: Pendiente, Aprobada, Rechazada
- Términos de pago configurables
- Numeración automática

**Datos personalizables:**

- Empresa: Nombre, RUT, Giro, Dirección, etc.
- Cliente: Precargados desde servicio

---

# Módulo de Cotizaciones (2)

## Gestión de Cotizaciones

**Funcionalidades avanzadas:**

- Generación de PDF profesional
- Envío por correo electrónico
- Duplicación de cotizaciones
- Edición posterior
- Eliminación con recalculación

**Ítems personalizables:**

- Descripción, Cantidad, Precio Unitario
- Total por ítem automático
- Múltiples categorías

**Términos:**

- Forma de pago: Transferencia, Efectivo, Cheque, Tarjeta
- Plazo: Al contado, 15, 30, 45, 60, 90 días

---

# Características Destacadas

## Funcionalidades Especiales

**Interfaz:**

- Diseño responsive (móviles y tablets)
- Tema claro y oscuro
- Menú lateral colapsable
- Búsquedas en tiempo real

**Validaciones:**

- Frontend y backend
- Mensajes descriptivos
- Validación de archivos

**Automatizaciones:**

- Cálculos matemáticos automáticos
- Numeración de cotizaciones
- Optimización de imágenes
- Actualización de totales en tiempo real

---

# Flujo de Trabajo

## Flujo Típico de Uso

1. **Registrar Cliente** - Ingresar datos básicos
2. **Registrar Vehículo** - Asociar al cliente
3. **Crear Servicio** - Describir trabajo a realizar
4. **Adjuntar Documentos/Fotos** - Evidencia del trabajo
5. **Generar Cotización** - Agregar ítems y precios
6. **Generar PDF y Enviar** - Documento profesional

---

# Demostración en Vivo

## Demo del Sistema

**Lo que vamos a mostrar:**

1. Crear un cliente nuevo
2. Registrar su vehículo
3. Generar una orden de servicio
4. Crear cotización con múltiples ítems
5. Generar PDF profesional
6. Cambiar estado de cotización

**Tiempo estimado:** 8-10 minutos

---

# Pruebas Realizadas

## Validación del Sistema

**Tipos de pruebas:**

- Pruebas funcionales por módulo
- Pruebas de integración (flujo completo)
- Pruebas de validación de formularios
- Pruebas de generación de PDF
- Pruebas de carga de archivos

**Resultados:**

- Todos los casos principales: OK
- Validaciones funcionando correctamente
- Cálculos automáticos verificados

**Responsable:** Persona 1 - Pruebas

---

# Instalación y Despliegue

## Cómo Instalar el Sistema

**Requisitos:**

- Python 3.13+
- MySQL 8.0
- Navegador web moderno

**Pasos:**

1. Clonar repositorio
2. Crear entorno virtual
3. Instalar dependencias
4. Configurar base de datos
5. Ejecutar migraciones
6. Crear superusuario
7. Ejecutar servidor

**Responsable:** Persona 2 - Instalación y entorno

---

# Mantención y Futuro

## Plan de Mantención

**Mantención Correctiva:**

- Corrección de bugs detectados

**Mantención Preventiva:**

- Actualización de dependencias
- Backups periódicos

**Mantención Adaptativa:**

- Nuevos campos o módulos

**Mantención Perfectiva:**

- Mejoras de rendimiento
- Optimización de interfaz

**Responsable:** Persona 4 - Mantención y cambios futuros

---

# Cambios Futuros

## Próximas Funcionalidades

**Mejoras planificadas:**

- Dashboard con estadísticas y gráficos
- Reportes de servicios por período
- Sistema de inventario de repuestos
- Notificaciones automáticas
- App móvil nativa
- Integración con pagos online
- Recordatorios de mantención
- Sistema de citas online

---

# Equipo y Responsabilidades

## Distribución del Trabajo

**Juan Pablo Maldonado Huenulef**

- Pruebas y validación

**Maximiliano Javier Beltrán Barrueto**

- Instalación y entorno

**Marcos Ignacio Villarroel Solís**

- Documentación y demo

**Benjamín Manuel Ignacio Moreira Arias**

- Mantención y coordinación

---

# Lecciones Aprendidas

## Aprendizajes del Proyecto

**Técnicos:**

- Implementación de patrón MVT con Django
- Gestión de relaciones en base de datos
- Validaciones frontend y backend
- Generación dinámica de PDFs

**Metodológicos:**

- Trabajo en equipo distribuido
- Gestión por historias de usuario
- Importancia de la documentación

**Profesionales:**

- Comunicación efectiva
- Cumplimiento de plazos
- Adaptación a cambios

---

# Conclusiones

## Logros Alcanzados

**Logros:**

- Sistema funcional y completo
- Interfaz intuitiva y profesional
- Documentación exhaustiva
- Código limpio y mantenible
- Pruebas exitosas

**Valor del proyecto:**

- Solución real a problema de talleres
- Automatización de procesos
- Base sólida para ampliaciones

**Cumplimiento:**

- Todos los criterios de la rúbrica cumplidos
- Sistema listo para producción

---

# ¿Preguntas?

## Contacto del Equipo

**Email:** soporte.tallermec@gmail.com

**Teléfono:** +56 9 8765 4321

**Repositorio:** GitHub: Cookeing/taller_mecanico

**Agradecimientos:** Gracias por su atención.
