import sqlite3
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
from numbers import Real

import pymysql

from domain.destination import Destination
from persistance.connection import open_connection, prefix_sql


class DestinationError(Exception):
    """Base exception for destination persistence operations."""


class DestinationValidationError(DestinationError, ValueError):
    """Raised when destination data does not satisfy the persistence rules."""


class DestinationNotFoundError(DestinationError, LookupError):
    """Raised when a destination with the requested ID does not exist."""


class DestinationPersistenceError(DestinationError, RuntimeError):
    """Raised when a database operation fails."""


class DestinationInUseError(DestinationPersistenceError):
    """Raised when a destination is still referenced by another record."""


@contextmanager
def _database_connection():
    connection = None
    try:
        connection = open_connection()
        yield connection
        connection.commit()
    except DestinationError:
        if connection is not None:
            connection.rollback()
        raise
    except (sqlite3.IntegrityError, pymysql.err.IntegrityError) as error:
        if connection is not None:
            connection.rollback()
        if _is_foreign_key_violation(error):
            raise DestinationInUseError(
                "No se puede eliminar el destino porque está asociado a otros registros."
            ) from error
        raise DestinationPersistenceError(
            "No se pudieron guardar los cambios del destino."
        ) from error
    except (sqlite3.Error, pymysql.MySQLError) as error:
        if connection is not None:
            connection.rollback()
        raise DestinationPersistenceError(
            "Ocurrió un error al acceder a los destinos."
        ) from error
    finally:
        if connection is not None:
            connection.close()


def _is_foreign_key_violation(error):
    if isinstance(error, sqlite3.IntegrityError):
        return "foreign key" in str(error).lower()
    return bool(error.args) and error.args[0] == 1451


def _validate_id(destination_id):
    if isinstance(destination_id, bool) or not isinstance(destination_id, int):
        raise DestinationValidationError("El ID del destino debe ser un número entero.")
    if destination_id <= 0:
        raise DestinationValidationError("El ID del destino debe ser mayor que cero.")


def _validate_destination(destination, require_id=False):
    if not isinstance(destination, Destination):
        raise DestinationValidationError(
            "El registro debe ser una instancia de Destination."
        )

    if require_id:
        _validate_id(destination.destination_id)
    elif destination.destination_id is not None:
        raise DestinationValidationError(
            "El ID debe estar vacío al crear un destino."
        )

    for field, value, max_length in (
        ("nombre", destination.name, 100),
        ("país", destination.country, 50),
        ("estado", destination.status, 10),
    ):
        if not isinstance(value, str):
            raise DestinationValidationError(
                f"El {field} del destino debe ser texto."
            )
        if not value.strip():
            raise DestinationValidationError(
                f"El {field} del destino es obligatorio."
            )
        if len(value) > max_length:
            raise DestinationValidationError(
                f"El {field} del destino no puede superar {max_length} caracteres."
            )

    if destination.description is not None and not isinstance(
        destination.description, str
    ):
        raise DestinationValidationError(
            "La descripción del destino debe ser texto o estar vacía."
        )

    if isinstance(destination.base_price, bool) or not isinstance(
        destination.base_price, (Real, Decimal)
    ):
        raise DestinationValidationError(
            "El precio base debe ser un número válido."
        )

    try:
        price = Decimal(str(destination.base_price))
        if not price.is_finite() or price < 0:
            raise DestinationValidationError(
                "El precio base debe ser un número finito no negativo."
            )
        if price > Decimal("99999999.99"):
            raise DestinationValidationError(
                "El precio base no puede superar 99999999.99."
            )
        if price != price.quantize(Decimal("0.01")):
            raise DestinationValidationError(
                "El precio base admite como máximo dos decimales."
            )
    except InvalidOperation as error:
        raise DestinationValidationError(
            "El precio base debe ser un número válido con hasta dos decimales."
        ) from error


def _destination_from_row(row):
    return Destination(
        destination_id=row[0],
        name=row[1],
        country=row[2],
        description=row[3],
        base_price=float(row[4]),
        status=row[5],
    )


def create_destination(destination):
    _validate_destination(destination)
    placeholder = prefix_sql()
    query = f"""
        INSERT INTO destination (name, country, description, base_price, status)
        VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
    """

    with _database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            query,
            (
                destination.name,
                destination.country,
                destination.description,
                float(Decimal(str(destination.base_price))),
                destination.status,
            ),
        )
        destination_id = cursor.lastrowid

    destination.destination_id = destination_id
    return destination


def get_destination_by_id(destination_id):
    _validate_id(destination_id)
    placeholder = prefix_sql()
    query = f"""
        SELECT destination_id, name, country, description, base_price, status
        FROM destination
        WHERE destination_id = {placeholder}
    """

    with _database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (destination_id,))
        row = cursor.fetchone()

    if row is None:
        raise DestinationNotFoundError(
            f"No se encontró el destino con ID {destination_id}."
        )
    return _destination_from_row(row)


def get_all_destinations():
    query = """
        SELECT destination_id, name, country, description, base_price, status
        FROM destination
        ORDER BY destination_id
    """

    with _database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return [_destination_from_row(row) for row in rows]


def update_destination(destination):
    _validate_destination(destination, require_id=True)
    placeholder = prefix_sql()
    query = f"""
        UPDATE destination
        SET name = {placeholder},
            country = {placeholder},
            description = {placeholder},
            base_price = {placeholder},
            status = {placeholder}
        WHERE destination_id = {placeholder}
    """

    with _database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            query,
            (
                destination.name,
                destination.country,
                destination.description,
                float(Decimal(str(destination.base_price))),
                destination.status,
                destination.destination_id,
            ),
        )
        if cursor.rowcount == 0:
            cursor.execute(
                f"SELECT 1 FROM destination WHERE destination_id = {placeholder}",
                (destination.destination_id,),
            )
            if cursor.fetchone() is None:
                raise DestinationNotFoundError(
                    f"No se encontró el destino con ID {destination.destination_id}."
                )

    return destination


def delete_destination(destination_id):
    _validate_id(destination_id)
    placeholder = prefix_sql()
    query = f"DELETE FROM destination WHERE destination_id = {placeholder}"

    with _database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (destination_id,))
        if cursor.rowcount == 0:
            raise DestinationNotFoundError(
                f"No se encontró el destino con ID {destination_id}."
            )
