class Destination:
    def __init__(
        self,
        name: str,
        country: str,
        base_price: float,
        status: str,
        description: str | None = "",
        destination_id: int | None = None,
    ):
        self._destination_id = destination_id
        self._name = name
        self._country = country
        self._description = description
        self._base_price = base_price
        self._status = status

    @property
    def destination_id(self) -> int | None:
        return self._destination_id

    @destination_id.setter
    def destination_id(self, value: int | None):
        self._destination_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str):
        self._country = value

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None):
        self._description = value

    @property
    def base_price(self) -> float:
        return self._base_price

    @base_price.setter
    def base_price(self, value: float):
        self._base_price = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value