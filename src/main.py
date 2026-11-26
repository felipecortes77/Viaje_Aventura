from persistance.create_db import create_tables
from presentation.destination_menu import run_destination_menu


def main():
    create_tables()
    print("Base de datos preparada correctamente.")
    run_destination_menu()


if __name__ == "__main__":
    main()