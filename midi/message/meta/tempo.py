from meta_message import MetaMessage


class Tempo(MetaMessage):
    def __init__(self, timestamp=0, tempo):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF 51 03')
        self.tempo = tempo.to_bytes(3, 'big')

    def data(self):
        return self.tempo
