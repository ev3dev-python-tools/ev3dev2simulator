class DataRequest:

    def __init__(self, address: str):
        self.address = address


    def serialize(self) -> dict:
        return {'type': 'DataRequest', 'address': self.address}
