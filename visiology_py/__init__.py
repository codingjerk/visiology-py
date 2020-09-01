from typing import NamedTuple


class Connection(NamedTuple):
    schema: str
    host: str
    username: str
    password: str
