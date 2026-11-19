# Viajes Aventura - Sistema de Gestión de Reservas Turísticas

Sistema de gestión para la agencia **Viajes Aventura**, diseñado para administrar destinos turísticos, armar paquetes personalizados, controlar la disponibilidad de cupos y gestionar el registro, acceso y reservas de los clientes.

---

## Contexto del Proyecto

Este proyecto responde al requerimiento operativo de la agencia **Viajes Aventura**, cubriendo tres módulos fundamentales del negocio:

* **Destinos:** Permite registrar, modificar, eliminar y listar los distintos destinos turísticos ofrecidos por la agencia, junto con su país, descripción, precio base y estado.
* **Paquetes:** Permite combinar múltiples destinos en un mismo paquete, definir fechas de inicio y término, calcular costos totales (incluyendo impuestos y cargos adicionales) y consultar la disponibilidad de cupos en tiempo real.
* **Reservas y Acceso:** Permite a los clientes registrarse en la plataforma, iniciar sesión de forma segura, reservar cupos en paquetes disponibles y consultar su historial completo de reservas.

---

## Modelo de Datos

Para garantizar que un cliente pueda recuperar y consultar sus reservas en cualquier momento, la base de datos persiste la relación entre el usuario, el paquete adquirido y los detalles de la transacción mediante **5 entidades principales**:

| Tabla | Descripción |
| :--- | :--- |
| **`client`** | Almacena la información de acceso y registro de los clientes (`client_id`, `name`, `email`, `password_hash`, `register_date`). |
| **`destination`** | Contiene el catálogo de destinos disponibles (`destination_id`, `name`, `country`, `description`, `base_price`, `status`). |
| **`package`** | Define los paquetes turísticos, fechas, cupos totales/disponibles, porcentaje de impuesto (`tax_pct`) y costos. |
| **`package_destination`** | Tabla intermedia que resuelve la relación muchos a muchos entre paquetes y destinos. |
| **`reservation`** | Registra cada reserva realizada por un cliente (`reservation_code`, `spots_quantity`, `total_cost`, `reservation_date`, `status`). |

---

## Estructura del Proyecto

```text
viajes-aventura/
├── persistance/
│   ├── connection.py        # Configuración y apertura de conexión (SQLite / MySQL)
│   └── create_tables.py     # Script de inicialización del esquema de base de datos
├── models/                  # Clases de dominio (Client, Destination, Package, Reservation)
├── services/                # Lógica de negocio (cálculo de costos, validación de cupos, auth)
├── main.py                  # Punto de entrada de la aplicación
└── README.md                # Documentación del proyecto
```

---

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd viajes-aventura
   ```

2. **Configurar el motor de base de datos:**
   El sistema soporta ejecución dual para **SQLite** (entorno local/pruebas) y **MySQL/MariaDB** (producción) a través del módulo `persistance/connection.py`.

3. **Inicializar las tablas:**
   Ejecuta el script de creación de tablas para preparar el esquema antes de iniciar el sistema:
   ```bash
   python -m persistance.create_tables
   ```
   Si todo se ejecuta correctamente, verás el mensaje:
   `Base de datos preparada correctamente.`

---

## Funcionalidades Principales

* **Seguridad de acceso:** Almacenamiento de contraseñas mediante hash (`password_hash`) y validación de correo único por cliente.
* **Integridad referencial:** Validación estricta de claves foráneas (`PRAGMA foreign_keys = ON` en SQLite) para evitar reservas huérfanas o paquetes sin destinos válidos.
* **Trazabilidad de reservas:** Generación de un código único de reserva (`reservation_code`), fecha exacta y estado (`confirmada`, `pendiente`, `cancelada`) para facilitar consultas e historial.
