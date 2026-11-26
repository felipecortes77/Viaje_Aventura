from typing import List, Optional

from domain.user import User
from persistance.connection import open_connection, prefix_sql


class UserDAO:
    @staticmethod
    def _to_user(row) -> User:
        return User(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            str(row[5]),
        )

    def create(self, user: User) -> User:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO user "
                f"(role_id, name, email, password_hash, registration_date) "
                f"VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
                (
                    user.role_id,
                    user.name,
                    user.email,
                    user.password_hash,
                    user.registration_date,
                ),
            )
            user_id = cursor.lastrowid
            connection.commit()
            return User(
                user_id,
                user.role_id,
                user.name,
                user.email,
                user.password_hash,
                user.registration_date,
            )
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def get_by_id(self, user_id: int) -> Optional[User]:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT user_id, role_id, name, email, password_hash, registration_date "
                f"FROM user WHERE user_id = {placeholder}",
                (user_id,),
            )
            row = cursor.fetchone()
            return self._to_user(row) if row is not None else None
        finally:
            connection.close()

    def get_by_email(self, email: str) -> Optional[User]:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT user_id, role_id, name, email, password_hash, registration_date "
                f"FROM user WHERE email = {placeholder}",
                (email,),
            )
            row = cursor.fetchone()
            return self._to_user(row) if row is not None else None
        finally:
            connection.close()

    def get_all(self) -> List[User]:
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT user_id, role_id, name, email, password_hash, registration_date "
                "FROM user ORDER BY user_id"
            )
            return [self._to_user(row) for row in cursor.fetchall()]
        finally:
            connection.close()

    def update(self, user: User) -> bool:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE user SET role_id = {placeholder}, name = {placeholder}, "
                f"email = {placeholder}, password_hash = {placeholder}, "
                f"registration_date = {placeholder} WHERE user_id = {placeholder}",
                (
                    user.role_id,
                    user.name,
                    user.email,
                    user.password_hash,
                    user.registration_date,
                    user.id,
                ),
            )
            updated = cursor.rowcount > 0
            connection.commit()
            return updated
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def delete(self, user_id: int) -> bool:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM user WHERE user_id = {placeholder}",
                (user_id,),
            )
            deleted = cursor.rowcount > 0
            connection.commit()
            return deleted
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()