from persistance.connection import open_connection, get_engine


def create_tables():
    connection = None
    try:
        connection = open_connection()
        cursor = connection.cursor()

        if get_engine() == "sqlite":
            cursor.execute("PRAGMA foreign_keys = ON;")

            sql_role = '''
                CREATE TABLE IF NOT EXISTS role (
                    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT
                )
            '''
            sql_user = '''
                CREATE TABLE IF NOT EXISTS user (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    registration_date DATE NOT NULL,
                    FOREIGN KEY (role_id) REFERENCES role(role_id)
                )
            '''
            sql_package = '''
                CREATE TABLE IF NOT EXISTS package (
                    package_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    total_spots INTEGER NOT NULL,
                    available_spots INTEGER NOT NULL,
                    tax_pct REAL NOT NULL,
                    additional_fees REAL,
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
                    place TEXT NOT NULL,
                    visit_start_date DATE NOT NULL,
                    visit_end_date DATE NOT NULL,
                    status TEXT NOT NULL,
                    PRIMARY KEY (package_id, destination_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id),
                    FOREIGN KEY (destination_id) REFERENCES destination(destination_id)
                )
            '''
            sql_booking = '''
                CREATE TABLE IF NOT EXISTS booking (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    package_id INTEGER NOT NULL,
                    booking_code TEXT NOT NULL,
                    spot_quantity INTEGER NOT NULL,
                    total_cost REAL NOT NULL,
                    booking_date DATETIME NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(user_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id)
                )
            '''
        else:
            sql_role = '''
                CREATE TABLE IF NOT EXISTS role (
                    role_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    description VARCHAR(255)
                )
            '''
            sql_user = '''
                CREATE TABLE IF NOT EXISTS user (
                    user_id INT PRIMARY KEY AUTO_INCREMENT,
                    role_id INT NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    registration_date DATE NOT NULL,
                    FOREIGN KEY (role_id) REFERENCES role(role_id)
                )
            '''
            sql_package = '''
                CREATE TABLE IF NOT EXISTS package (
                    package_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    total_spots INT NOT NULL,
                    available_spots INT NOT NULL,
                    tax_pct DECIMAL(4,2) NOT NULL,
                    additional_fees DECIMAL(10,2),
                    total_cost DECIMAL(10,2) NOT NULL
                )
            '''
            sql_destination = '''
                CREATE TABLE IF NOT EXISTS destination (
                    destination_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    country VARCHAR(50) NOT NULL,
                    description TEXT,
                    base_price DECIMAL(10,2) NOT NULL,
                    status VARCHAR(10) NOT NULL
                )
            '''
            sql_package_destination = '''
                CREATE TABLE IF NOT EXISTS package_destination (
                    package_id INT NOT NULL,
                    destination_id INT NOT NULL,
                    place VARCHAR(100) NOT NULL,
                    visit_start_date DATE NOT NULL,
                    visit_end_date DATE NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    PRIMARY KEY (package_id, destination_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id),
                    FOREIGN KEY (destination_id) REFERENCES destination(destination_id)
                )
            '''
            sql_booking = '''
                CREATE TABLE IF NOT EXISTS booking (
                    booking_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    package_id INT NOT NULL,
                    booking_code VARCHAR(20) NOT NULL,
                    spot_quantity INT NOT NULL,
                    total_cost DECIMAL(10,2) NOT NULL,
                    booking_date DATETIME NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(user_id),
                    FOREIGN KEY (package_id) REFERENCES package(package_id)
                )
            '''

        cursor.execute(sql_role)
        cursor.execute(sql_user)
        cursor.execute(sql_package)
        cursor.execute(sql_destination)
        cursor.execute(sql_package_destination)
        cursor.execute(sql_booking)

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