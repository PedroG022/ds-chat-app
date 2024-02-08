import uuid


class ClientIdentifier:
    def __init__(self, name: str):
        self.client_id: uuid = uuid.uuid4()
        self.name: str = name
