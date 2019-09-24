class SoundCommand:

    def __init__(self, message: str):
        self.message = message


    def serialize(self) -> dict:
        return {
            'type': 'SoundCommand',
            'message': self.message
        }
