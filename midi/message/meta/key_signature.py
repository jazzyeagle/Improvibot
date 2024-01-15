from meta_message import MetaMessage


class KeySignature(MetaMessage):
    def __init__(self, timestamp=0, sharps_flats, major_minor):
        super().__init__(timestamp)
        self._event_code  = bytes.fromhex('FF 59 02')
        self.sharps_flats = sharps_flats.to_bytes(1, 'big')
        self.major_minor  = major_minor.to_bytes(1, 'big')


    def data(self):
        return  self.sharps_flats + \
                self.major_minor
















































































