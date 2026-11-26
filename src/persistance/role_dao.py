from typing import List, Optional

from domain.role import Role
from persistance.connection import open_connection, prefix_sql


class RoleDAO:
    @staticmethod
    def _to_role(row) -> Role:
        return Role(row[0], row[1], row[2])

    def create(self, role: Role) -> Role:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO role (name, description) VALUES ({placeholder}, {placeholder})",
                (role.name, role.description),
            )
            role_id = cursor.lastrowid
            connection.commit()
            return Role(role_id, role.name, role.description)
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def get_by_id(self, role_id: int) -> Optional[Role]:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT role_id, name, description FROM role WHERE role_id = {placeholder}",
                (role_id,),
            )
            row = cursor.fetchone()
            return self._to_role(row) if row is not None else None
        finally:
            connection.close()

    def get_by_name(self, name: str) -> Optional[Role]:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT role_id, name, description FROM role WHERE name = {placeholder}",
                (name,),
            )
            row = cursor.fetchone()
            return self._to_role(row) if row is not None else None
        finally:
            connection.close()

    def get_all(self) -> List[Role]:
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT role_id, name, description FROM role ORDER BY role_id")
            return [self._to_role(row) for row in cursor.fetchall()]
        finally:
            connection.close()

    def update(self, role: Role) -> bool:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE role SET name = {placeholder}, description = {placeholder} "
                f"WHERE role_id = {placeholder}",
                (role.name, role.description, role.id),
            )
            updated = cursor.rowcount > 0
            connection.commit()
            return updated
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def delete(self, role_id: int) -> bool:
        placeholder = prefix_sql()
        connection = open_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM role WHERE role_id = {placeholder}",
                (role_id,),
            )
            deleted = cursor.rowcount > 0
            connection.commit()
            return deleted
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()