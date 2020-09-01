import visiology_py as vi
import requests


class ApiV2:
    def __init__(self, connection: vi.Connection, requests=requests) -> None:
        self.connection = connection
        self.requests = requests
