from persistance.connection import open_connection, get_engine


def create_tables():
    connection = None
    try:
        connection = open_connection()
        cursor = connection.cursor()

        if get_engine() == "sqlite":
            cursor.execute("PRAGMA foreign_keys = ON;")

            sql_client = '''
                CREATE TABLE IF NOT EXISTS client (
                    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    register_date DATETIME NOT NULL
                )
            '''
            sql_package = '''
                CREATE TABLE IF NOT EXISTS package (
                    package_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    start_date DATETIME NOT NULL,
                    end_date DATETIME NOT NULL,
                    total_spots INTEGER NOT NULL,
                    available_spots INTEGER NOT NULL,
                    tax_pct REAL NOT NULL,
                    additional_charges REAL,
                    total_cost REAL NOT NULL
                )
            '''
            sql_destination = '''
                CREATE TABLE IF NOT EXISTS destination (
                    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    country TEXT NOT NULL,
                    description TEXT,
                    base_price REAL NOT NULL,
                    status TEXT NOT NULL
                )
            '''
            sql_package_destination = '''
                CREATE TABLE IF NOT EXISTS package_destination (
                    package_id INTEGER NOT NULL,
                    destination_id INTEGER NOT NULL,
                    PRIMARY KEY (package_id, destination_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id),
                    FOREIGN KEY (destination_id) REFERENCES destination(destination_id)
                )
            '''
            sql_reservation = '''
                CREATE TABLE IF NOT EXISTS reservation (
                    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER NOT NULL,
                    package_id INTEGER NOT NULL,
                    reservation_code TEXT NOT NULL,
                    spots_quantity INTEGER NOT NULL,
                    total_cost REAL NOT NULL,
                    reservation_date DATETIME NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (client_id) REFERENCES client(client_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id)
                )
            '''
        else:
            sql_client = '''
                CREATE TABLE IF NOT EXISTS client (
                    client_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    register_date DATETIME NOT NULL
                )
            '''
            sql_package = '''
                CREATE TABLE IF NOT EXISTS package (
                    package_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    start_date DATETIME NOT NULL,
                    end_date DATETIME NOT NULL,
                    total_spots INT NOT NULL,
                    available_spots INT NOT NULL,
                    tax_pct DECIMAL(4,2) NOT NULL,
                    additional_charges DECIMAL(10,2),
                    total_cost DECIMAL(10,2) NOT NULL
                )
            '''
            sql_destination = '''
                CREATE TABLE IF NOT EXISTS destination (
                    destination_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    country VARCHAR(60) NOT NULL,
                    description TEXT,
                    base_price DECIMAL(10,2) NOT NULL,
                    status VARCHAR(10) NOT NULL
                )
            '''
            sql_package_destination = '''
                CREATE TABLE IF NOT EXISTS package_destination (
                    package_id INT NOT NULL,
                    destination_id INT NOT NULL,
                    PRIMARY KEY (package_id, destination_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id),
                    FOREIGN KEY (destination_id) REFERENCES destination(destination_id)
                )
            '''
            sql_reservation = '''
                CREATE TABLE IF NOT EXISTS reservation (
                    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
                    client_id INT NOT NULL,
                    package_id INT NOT NULL,
                    reservation_code VARCHAR(20) NOT NULL,
                    spots_quantity INT NOT NULL,
                    total_cost DECIMAL(10,2) NOT NULL,
                    reservation_date DATETIME NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    FOREIGN KEY (client_id) REFERENCES client(client_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id)
                )
            '''

        # Ordered creation respecting foreign key dependencies
        cursor.execute(sql_client)
        cursor.execute(sql_package)
        cursor.execute(sql_destination)
        cursor.execute(sql_package_destination)
        cursor.execute(sql_reservation)

        connection.commit()

    except Exception:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    create_tables()
    print("Base de datos preparada correctamente.")
