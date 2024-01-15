from base import Base


class Message(Base):
    def __init__(self):
        self._event_code = b''

    def data(self):
        return NotImplementedError

    def size_to_bytes(self, value):
        return value.to_bytes(length=((value.bit_length() // 8) + 1))

    def get_note_length(self, encoding, ticks, bpm, sample_rate):
        if encoding = Base.Encoding.MIDI:
            return ticks * self.time
        else:
            # JACK
            return (sample_rate / bpm) * self.time
