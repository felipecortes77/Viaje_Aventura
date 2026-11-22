# Viajes Aventura

Proyecto inicial para la gestión de reservas turísticas de **Viajes Aventura**.
Actualmente incluye la configuración de la conexión a la base de datos y la
creación del esquema relacional para clientes, destinos, paquetes y reservas.

## Estado actual

La aplicación actualmente:

- Abre una conexión usando SQLite o MySQL/MariaDB.
- Activa las claves foráneas cuando se utiliza SQLite.
- Crea las tablas necesarias para el sistema.
- Mantiene la relación entre paquetes y destinos mediante una tabla intermedia.

Todavía no están implementados los servicios de registro, autenticación,
administración de destinos y paquetes, ni la creación y consulta de reservas.

## Estructura del proyecto

```text
Viaje_Aventura/
├── .env.example
├── README.md
├── requirements.txt
├── docs/
│   ├── Modelo fisico y requerimientos.pdf
│   └── ia.txt
└── src/
    ├── main.py
    └── persistance/
        ├── connection.py
        ├── create_db.py
        └── seed_db.py
```

## Modelo de datos

El esquema creado por `src/persistance/create_db.py` contiene cinco tablas:

| Tabla | Propósito |
| --- | --- |
| `client` | Datos del cliente, correo y campo para la contraseña almacenada como hash. |
| `destination` | Catálogo de destinos, país, descripción, precio base y estado. |
| `package` | Paquetes, fechas, cupos, impuestos, cargos adicionales y costo total. |
| `package_destination` | Relación muchos a muchos entre paquetes y destinos. |
| `reservation` | Cliente, paquete, código, cantidad de cupos, costo, fecha y estado de la reserva. |

Las tablas `package_destination` y `reservation` tienen claves foráneas para
mantener la integridad de las relaciones.

## Descargar el proyecto y trabajar con ramas

Abre **Git Bash** y ejecuta:

```bash
git clone https://github.com/felipecortes77/Viaje_Aventura.git
cd Viaje_Aventura
```

Para crear una rama nueva y cambiarte a ella:

```bash
git switch -c tipo/descripcion-corta
```

Usa el prefijo según el propósito del cambio:

- `feature/`: agregar una funcionalidad.
- `fix/`: corregir un error.
- `docs/`: crear o actualizar documentación.

Por ejemplo:

```bash
git switch -c docs/actualizar-readme
```

Para cambiar a una rama existente:

```bash
git switch main
```

## Requisitos

- Python 3
- Dependencias incluidas en `requirements.txt`
- SQLite para desarrollo local, o MySQL/MariaDB para otro entorno

## Instalación

Desde la carpeta raíz del proyecto:

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

En macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración

La configuración se lee desde un archivo `.env`. Se puede partir de
`.env.example`.

Para SQLite:

```env
DB_ENGINE=sqlite
DB_NAME=ecotech.db
```

Para MySQL:

```env
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=viajes_aventura
```

Si no se define `DB_ENGINE`, se utiliza SQLite. En SQLite, si no se define
`DB_NAME`, el archivo utilizado por defecto es `ecotech.db`.

## Ejecución

Para crear las tablas y comprobar la conexión:

```powershell
python src\persistance\create_db.py
```

También se puede ejecutar el punto de entrada actual:

```powershell
python src\main.py
```

Ambos comandos ejecutan `create_tables()`. El script de creación de tablas
informa `Base de datos preparada correctamente.` cuando termina correctamente.

## Dependencias principales

- `python-dotenv`: carga las variables de configuración desde `.env`.
- `PyMySQL`: conexión con MySQL/MariaDB.
- `bcrypt`: disponible para el almacenamiento seguro de contraseñas cuando se
  implemente el módulo de autenticación.
