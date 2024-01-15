from midi.message import Message


class EndOfTrack(Message):
    def __init__(self, timestamp=0):
        super().__init__(timestamp)
        self._event_code = bytes.fromhex('FF2F00')

    # Return empty, as there is no data associated with
    #    this message.
    def data(self):
        return b''
