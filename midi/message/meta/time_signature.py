from meta_message import MetaMessage


class TimeSignature(MetaMessage):
    def __init__(self, timestamp=0, num_beats, beat_note, clocks, num_32nd_notes):
        super().__init__(timestamp)
        self._event_code    = bytes.fromhex('FF 58 04')
        self.num_beats      = num_beats.to_bytes(1, 'big')
        self.beat_note      = beat_note.to_bytes(1, 'big')
        self.clocks         = clocks.to_bytes(1, 'big')
        self.num_32nd_notes = num_32nd_notes.to_bytes(1, 'big')


    def data(self):
        return  self.num_beats + \
                self.beat_note + \
                self.clocks    + \
                self.num_32nd_notes















































































