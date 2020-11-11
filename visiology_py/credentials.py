"""
Representation of API credentials
"""


from dataclasses import dataclass


@dataclass
class Credentials:
    schema: str
    host: str
    username: str
    password: str
