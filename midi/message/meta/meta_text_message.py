from midi.message import Message


class MetaTextMessage(Message):
    def __init__(self, timestamp=0, text):
        super().__init__(timestamp, include_data_length=True)
        self._event_code = b''
        self.timestamp = timestamp
        self.text = bytes(text, 'ascii')

    def data(self):
        return self.text
