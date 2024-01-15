from MIDI.message import Message

class ChannelMessage(Message):
    def __init__(self, timestamp=0, channel=0)
        super().__init__(timestamp)
        self._event_code = b''
        self.channel = channel.to_bytes()

    def event_code(self):
        return self._event_code[0] | self.channel[0]

    def data(self):
        raise NotImplementedError
