from base      import Base
from functools import reduce
from format    import Format, FormatType
from division  import Division, DivisionType


class File(Base):
    def __init__(self, filename='', format_type, division_type, ticks=500000, bpm=120, sample_rate=44100):
        if not filename:
            self.filename = filename
            load(filename)
        else:
            self.format      = Format(format_type)
            self.division    = Division(division_type)
            self.tracks      = []
            self.ticks       = ticks
            self.bpm         = bpm
            self.sample_rate = sample_rate

    def set_ticks(self, ticks):
        self.ticks = ticks

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    # 10 = header size, 4 bytes for 'MThd' and 6 for the data
    def size(self):
        return reduce(lambda x, track: x + track.size(), tracks, 10)
        pass

    def encode(self, encoding)            
        return reduce(lambda x, track: x.append(track.encode()), tracks, encoder_header())

    def encode_header(self):
        b'MThd' + (6).to_bytes(2, 'big') 
                + self.format.encode()
                + len(self.tracks).to_bytes(2, 'big')
                + self.division.encode()

    def load(self, filename):
        pass

    def save(self, filename):
        pass
