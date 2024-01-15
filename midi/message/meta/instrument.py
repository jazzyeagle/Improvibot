from meta_text_message import MetaTextMessage


class Instrument(MetaTextMessage):
    def __init__(self, timestamp=0, text):
        super().__init__()
        self._event_code = bytes.fromhex('FF04')
