# Para ejecutar:
#### Desde la raíz del proyecto: 
- `python -m app.main` para linux

#### Estructura de carpetas:
```
.
├── app                     # Aplicación principal (organiza toda la lógica del sistema)
│   ├── controllers         # Orquesta la lógica: conecta requests/UI con servicios/modelos
│   │   └── product_controller.py
│   ├── core                # Configuración base del sistema (DB, inicialización, settings)
│   │   ├── database.py
│   │   └── init_db.py
│   ├── helpers             # Utilidades y funciones compartidas (ej: manejo de sesiones)
│   │   └── get_db.py
│   ├── main.py             # Punto de entrada de la aplicación
│   ├── models              # Definición de entidades ORM (tablas de la base de datos)
│   │   └── product.py
│   ├── schemas             # Esquemas de validación y transferencia de datos (Pydantic)
│   │   └── product_schema.py
│   └── views               # Capa de presentación (UI)
│       ├── components      # Componentes reutilizables de la interfaz
│       └── pages           # Vistas/páginas principales de la aplicación
│           └── home_view.py
├── data                    # Persistencia local (base de datos SQLite)
│   └── database.db
├── README.md               # Documentación del proyecto
└── requirements.txt        # Dependencias del proyecto
```