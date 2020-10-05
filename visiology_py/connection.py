from dataclasses import dataclass


@dataclass
class Connection:
    schema: str
    host: str
    username: str
    password: str
