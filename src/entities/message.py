from src.entities import ClientIdentifier


class Message:
    def __init__(self, body: str, identifier: ClientIdentifier = None):
        self.body: str = body
        self.identifier: ClientIdentifier = identifier
