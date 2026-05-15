# Minimarket ERP - Sistema de Gestión

Sistema de gestión integral para minimarkets y papelerías, desarrollado con Flet (Python).

## Módulos

### 1. Dashboard
Panel principal con visión general del negocio: métricas de ventas, productos activos, stock bajo y gastos mensuales. Incluye gráfico de rendimiento semanal.

### 2. Catálogo (Productos)
Gestión del inventario de productos. Permite agregar, editar, eliminar y buscar productos. Muestra tarjetas con imagen, precio, stock y acciones rápidas.

### 3. Kardex
Control de movimientos de inventario. Registra entradas y salidas de productos con motivo y documentación de referencia. Historial visual en tabla de datos.

### 4. Boletas
Módulo de ventas y facturación. Registro de transacciones con selección de productos, cálculo de totales y generación de boletas.

### 5. Gastos
Control de gastos operativos del negocio. Registro y categorización de gastos para análisis financiero.

### 6. Reportes
Generación de reportes y estadísticas del negocio. Visualización de datos históricos y análisis de rendimiento.

### 7. Sincronización
Gestión de sincronización de datos. Mantiene actualizada la información entre diferentes dispositivos o servidores.

---

## Características

- Interfaz moderna con soporte Light/Dark Mode
- Diseño responsivo para diferentes tamaños de pantalla
- Persistencia de datos en SQLite
- Tema visual profesional para papelerías

## Tecnologías

- **Frontend**: Flet (Python)
- **Backend**: Python
- **Base de datos**: SQLite

---

## Para ejecutar:

```bash
python -m app.main
```

## Estructura

```
app/
├── controllers/      # Lógica de negocio
├── core/            # Configuración y base de datos
├── models/          # Entidades de la base de datos
├── repositories/    # Acceso a datos
├── schemas/         # Validación de datos
├── services/        # Servicios del sistema
└── views/           # Interfaz de usuario
    ├── components/  # Componentes reutilizables
    └── pages/       # Vistas principales
```