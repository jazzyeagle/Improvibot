import logging
import MIDI


def hexify(b):
    return b.encode(MIDI.Encoding.MIDI).hex(' ').upper()


class TestMidiChannel:
    def test_note_on(self):
        note_on = MIDI.NoteOn(0, 0, 60, 127)
        logging.info(hexify(note_on))
        assert note_on.encode(
            MIDI.Encoding.MIDI) == bytes.fromhex('00 90 3C 7F')

    def test_note_off(self):
        note_off = MIDI.NoteOff(96, 1, 60, 64)
        logging.info(hexify(note_off))
        assert note_off.encode(
            MIDI.Encoding.MIDI) == bytes.fromhex('60 81 3C 40')

    def test_aftertouch(self):
        aftertouch = MIDI.Aftertouch(5, 9, 73)
        logging.info(hexify(aftertouch))
        assert aftertouch.encode(
            MIDI.Encoding.MIDI) == bytes.fromhex('05 D9 49')

    def test_control_change(self):
        cc = MIDI.ControlChange(103, 12, 18, 97)
        logging.info(hexify(cc))
        assert cc.encode(MIDI.Encoding.MIDI) == bytes.fromhex('67 BC 12 61')

    def test_pitch_bend(self):
        pb = MIDI.PitchBend(0, 1, 127)
        logging.info(hexify(pb))
        assert pb.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 E1 00 7F')

    def test_polyphonic_key(self):
        pk = MIDI.PolyphonicKey(0, 0, 69, 92)
        logging.info(hexify(pk))
        assert pk.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 A0 45 5C')

    def test_program_change(self):
        pc = MIDI.ProgramChange(42, 7, 19)
        logging.info(hexify(pc))
        assert pc.encode(MIDI.Encoding.MIDI) == bytes.fromhex('2A C7 13')
