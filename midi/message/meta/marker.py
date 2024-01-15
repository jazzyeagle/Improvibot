from meta_text_message import MetaTextMessage


class Marker(MetaTextMessage):
    def __init__(self, timestamp=0, text):
        super().__init__(timestamp, text)
        self._event_code = bytes.fromhex('FF06')
