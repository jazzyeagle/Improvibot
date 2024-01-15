from base import Base
from functools import reduce

class Track(Base):
    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)

    def encode(self, encoding, ticks=500000, bpm=120, sample_rate=44100):
        reduce(lambda x, message: x.append(message.to_bytes(encoding, ticks, bpm, sample_rate)), self.messages, bytearray())

    def size(self):
        return reduce(lambda x, message: x + message.length(), self.messages)
