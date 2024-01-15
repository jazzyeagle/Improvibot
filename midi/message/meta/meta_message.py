from midi.message import Message


class MetaMessage(Message):
    def __init__(self, timestamp=0, include_data_length=False):
        if type(timestamp) == 'bytes':
            self.timestamp = timestamp
        else:
            self.timestamp = timestamp.to_bytes()

        self.event_code = b''

        self.include_data_length = include_data_length

    def data(self):
        raise NotImplementedError
