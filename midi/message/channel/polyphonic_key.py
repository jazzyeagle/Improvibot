from channel_message import ChannelMessage


class PolyphonicKey(ChannelMessage):
    def __init__(self, timestamp, channel, note, pressure):
        super().__init__(timestamp, channel)
        self._event_code = (0xA0).to_bytes(1, 'big')
        self.note        = note.to_bytes(1, 'big')
        self.pressure    = pressure.to_bytes(1, 'big')

    def data(self):
        return bytes([self.note, self.pressure])
