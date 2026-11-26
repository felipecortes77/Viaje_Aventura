from domain.destination import Destination
from persistance.destination_dao import (
    DestinationInUseError,
    DestinationNotFoundError,
    DestinationPersistenceError,
    DestinationValidationError,
    create_destination,
    delete_destination,
    get_all_destinations,
    get_destination_by_id,
    update_destination,
)


def _read_required_text(label, max_length):
    while True:
        value = input(f"{label}: ").strip()
        if not value:
            print(f"El campo {label.lower()} es obligatorio.")
        elif len(value) > max_length:
            print(f"El campo {label.lower()} no puede superar {max_length} caracteres.")
        else:
            return value


def _read_destination_id():
    while True:
        try:
            destination_id = int(input("ID del destino: "))
            if not 0 < destination_id <= 2147483647:
                print("El ID debe estar entre 1 y 2147483647.")
            else:
                return destination_id
        except ValueError:
            print("Ingresa un ID numérico válido.")


def _read_destination_fields():
    name = _read_required_text("Nombre", 100)
    country = _read_required_text("País", 50)
    description = input("Descripción (opcional): ").strip()

    while True:
        try:
            base_price = float(input("Precio base: "))
            break
        except ValueError:
            print("Ingresa un precio numérico válido.")

    status = _read_required_text("Estado", 10)
    return name, country, description, base_price, status


def _show_destination(destination):
    print(
        f"ID: {destination.destination_id} | "
        f"Nombre: {destination.name} | País: {destination.country} | "
        f"Descripción: {destination.description or '-'} | "
        f"Precio base: {destination.base_price:.2f} | Estado: {destination.status}"
    )


def _add_destination():
    fields = _read_destination_fields()
    destination = Destination(
        name=fields[0],
        country=fields[1],
        description=fields[2],
        base_price=fields[3],
        status=fields[4],
    )
    saved_destination = create_destination(destination)
    print(f"Destino creado correctamente con ID {saved_destination.destination_id}.")


def _list_destinations():
    destinations = get_all_destinations()
    if not destinations:
        print("No hay destinos registrados.")
        return

    for destination in destinations:
        _show_destination(destination)


def _show_destination_by_id():
    destination = get_destination_by_id(_read_destination_id())
    _show_destination(destination)


def _edit_destination():
    destination_id = _read_destination_id()
    get_destination_by_id(destination_id)
    fields = _read_destination_fields()
    destination = Destination(
        destination_id=destination_id,
        name=fields[0],
        country=fields[1],
        description=fields[2],
        base_price=fields[3],
        status=fields[4],
    )
    update_destination(destination)
    print("Destino actualizado correctamente.")


def _remove_destination():
    destination_id = _read_destination_id()
    delete_destination(destination_id)
    print("Destino eliminado correctamente.")


def run_destination_menu():
    actions = {
        "1": _add_destination,
        "2": _list_destinations,
        "3": _show_destination_by_id,
        "4": _edit_destination,
        "5": _remove_destination,
    }

    while True:
        print(
            "\n=== Menú de destinos ===\n"
            "1. Crear destino\n"
            "2. Listar destinos\n"
            "3. Buscar destino por ID\n"
            "4. Actualizar destino\n"
            "5. Eliminar destino\n"
            "0. Salir"
        )
        option = input("Selecciona una opción: ").strip()

        if option == "0":
            print("Saliendo del menú de destinos.")
            return

        action = actions.get(option)
        if action is None:
            print("Opción no válida. Selecciona una opción del menú.")
            continue

        try:
            action()
        except DestinationValidationError as error:
            print(f"Datos inválidos: {error}")
        except DestinationNotFoundError as error:
            print(f"Destino no encontrado: {error}")
        except DestinationInUseError as error:
            print(f"No se puede eliminar el destino: {error}")
        except DestinationPersistenceError as error:
            print(f"Error de base de datos: {error}")
