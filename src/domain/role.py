class Role:
    def __init__(self, role_id: int, name: str, description: str = None):
        self._id = role_id
        self._name = name
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description