class User:
    def __init__(self, user_id: int, role_id: int, name: str, email: str, password_hash: str, registration_date: str):
        self._id = user_id
        self._role_id = role_id
        self._name = name
        self._email = email
        self._password_hash = password_hash
        self._registration_date = registration_date

    @property
    def id(self):
        return self._id

    @property
    def role_id(self):
        return self._role_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def password_hash(self):
        return self._password_hash

    @property
    def registration_date(self):
        return self._registration_date