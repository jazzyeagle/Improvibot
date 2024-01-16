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


class TestMidiMeta:
    def test_channel_prefix(self):
        cp = MIDI.ChannelPrefix(37291, 10)
        logging.info(hexify(cp))
        assert cp.encode(MIDI.Encoding.MIDI) == bytes.fromhex('91 AB FF 20 01 0A')

    def test_end_of_track(self):
        eot = MIDI.EndOfTrack()
        logging.info(hexify(eot))
        assert eot.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 2F 00')

    def test_key_signature(self):
        ks = MIDI.KeySignature(500000, -3, 1)
        logging.info(hexify(ks))
        assert ks.encode(MIDI.Encoding.MIDI) == bytes.fromhex('07 A1 20 FF 59 02 FD 01')

    def test_sequence_number(self):
        sn = MIDI.SequenceNumber(0, 2)
        logging.info(hexify(sn))
        assert sn.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 00 02 00 02')

    def test_smpte(self):
        smpte = MIDI.SMPTE(0, 10, 20, 30, 40, 50)
        logging.info(hexify(smpte))
        assert smpte.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 54 05 0A 14 1E 28 32')

    def test_tempo(self):
        tempo = MIDI.Tempo(0, 140)
        logging.info(hexify(tempo))
        assert tempo.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 51 03 00 00 8C')

    def test_time_signature(self):
        ts = MIDI.TimeSignature(0, 6, 8)
        logging.info(hexify(ts))
        assert ts.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 58 04 06 08 00 18')

    def test_track_number(self):
        tn = MIDI.TrackNumber(0, 5)
        logging.info(hexify(tn))
        assert tn.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 00 02 00 05')


class TestMidiMetaText:
    def test_copyright(self):
        copyright = MIDI.Copyright(0, '(c)2024 That\'s Some Record Label!')
        logging.info(hexify(copyright))
        assert copyright.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 02 21 28 63 29 32 30 32 34 20 54 68 61 74 27 73 20 53 6F 6D 65 20 52 65 63 6F 72 64 20 4C 61 62 65 6C 21')

    def test_cue_point(self):
        cp = MIDI.CuePoint(11, 'Verse 1')
        logging.info(hexify(cp))
        assert cp.encode(MIDI.Encoding.MIDI) == bytes.fromhex('0B FF 07 07 56 65 72 73 65 20 31')

    def test_instrument(self):
        i = MIDI.Instrument(5, 'Grand Piano')
        logging.info(hexify(i))
        assert i.encode(MIDI.Encoding.MIDI) == bytes.fromhex('05 FF 04 0B 47 72 61 6E 64 20 50 69 61 6E 6F')

    def test_lyric(self):
        l = MIDI.Lyric(123456789, 'Louisiana / Born on the bayou I go / Looking for crawdads')
        logging.info(hexify(l))
        assert l.encode(MIDI.Encoding.MIDI) == bytes.fromhex('07 5B CD 15 FF 05 39 4C 6F 75 69 73 69 61 6E 61 20 2F 20 42 6F 72 6E 20 6F 6E 20 74 68 65 20 62 61 79 6F 75 20 49 20 67 6F 20 2F 20 4C 6F 6F 6B 69 6E 67 20 66 6F 72 20 63 72 61 77 64 61 64 73')

    def test_marker(self):
        m = MIDI.Marker(0, 'Chorus')
        logging.info(hexify(m))
        assert m.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 06 06 43 68 6F 72 75 73')

    def test_sequence_name(self):
        sn = MIDI.SequenceName(0, 'Melody Sequence 1')
        logging.info(hexify(sn))
        assert sn.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 03 11 4D 65 6C 6F 64 79 20 53 65 71 75 65 6E 63 65 20 31')

    def test_text(self):
        t = MIDI.Text(0, 'Don\'t @ Me, Bruh!')
        logging.info(hexify(t))
        assert t.encode(MIDI.Encoding.MIDI) == bytes.fromhex('00 FF 01 11 44 6F 6E 27 74 20 40 20 4D 65 2C 20 42 72 75 68 21')

    def test_track_name(self):
        tn = MIDI.TrackName(text='The Cooliest Track Name')
        logging.info(hexify(tn))
        assert tn.encode(MIDI.Encoding.MIDI == bytes.fromhex('00 FF 03 17 54 68 65 20 43 6F 6F 6C 69 65 73 74 20 54 72 61 63 6B 20 4E 61 6D 65'))