from diff_match_patch import diff_match_patch
import logging
from MIDI import *


def hexify(message):
    return message.encode(Encoding.MIDI).hex(' ').upper()


class TestTrack:
    # Test data obtained from https://github.com/jazz-soft/test-midi-files/.
    #    This is the C Major test file with the header removed.
    #    There is also an extraneous 0A byte that I removed, as I cannot
    #    find anywhere in the MIDI docs that it is required.  Length bytes
    #    were adjusted accordingly as well.
    def test_track(self):
        track = Track()
        track.append(TrackName(text="C Major Scale Test"))
        track.append(Copyright(text="https://jazz-soft.net"))
        track.append(Text(text="This is the most basic MIDI test to serve a template for more useful tests."))
        track.append(Text(text="You must hear a C-Major scale."))
        track.append(Text(text=" Now you must hear C5!"))
        track.append(NoteOn(0, 0, 60, 127))
        track.append(NoteOff(96, 0, 60, 64))
        track.append(Text(text=" Now you must hear D5!"))
        track.append(NoteOn(0, 0, 62, 127))
        track.append(NoteOff(96, 0, 62, 64))
        track.append(Text(text=" Now you must hear E5!"))
        track.append(NoteOn(0, 0, 64, 127))
        track.append(NoteOff(96, 0, 64, 64))
        track.append(Text(text=" Now you must hear F5!"))
        track.append(NoteOn(0, 0, 65, 127))
        track.append(NoteOff(96, 0, 65, 64))
        track.append(Text(text=" Now you must hear G5!"))
        track.append(NoteOn(0, 0, 67, 127))
        track.append(NoteOff(96, 0, 67, 64))
        track.append(Text(text=" Now you must hear A5!"))
        track.append(NoteOn(0, 0, 69, 127))
        track.append(NoteOff(96, 0, 69, 64))
        track.append(Text(text=" Now you must hear B5!"))
        track.append(NoteOn(0, 0, 71, 127))
        track.append(NoteOff(96, 0, 71, 64))
        track.append(Text(text=" Now you must hear C6!"))
        track.append(NoteOn(0, 0, 72, 127))
        track.append(NoteOff(96, 0, 72, 64))
        track.append(Text(text="Thank you!"))
        track.append(EndOfTrack())

        calculated = track.encode(Encoding.MIDI)
        answer = bytes.fromhex('4d 54 72 6b 00 00 01 c2 00 ff 03 12 43 20 4d 61 6a 6f 72 20 53 63 61 6c 65 20 54 65 73 74 00 ff 02 15 68 74 74 70 73 3a 2f 2f 6a 61 7a 7a 2d 73 6f 66 74 2e 6e 65 74 00 ff 01 4b 54 68 69 73 20 69 73 20 74 68 65 20 6d 6f 73 74 20 62 61 73 69 63 20 4d 49 44 49 20 74 65 73 74 20 74 6f 20 73 65 72 76 65 20 61 20 74 65 6d 70 6c 61 74 65 20 66 6f 72 20 6d 6f 72 65 20 75 73 65 66 75 6c 20 74 65 73 74 73 2e 00 ff 01 1e 59 6f 75 20 6d 75 73 74 20 68 65 61 72 20 61 20 43 2d 4d 61 6a 6f 72 20 73 63 61 6c 65 2e 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 43 35 21 00 90 3c 7f 60 80 3c 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 44 35 21 00 90 3e 7f 60 80 3e 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 45 35 21 00 90 40 7f 60 80 40 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 46 35 21 00 90 41 7f 60 80 41 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 47 35 21 00 90 43 7f 60 80 43 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 41 35 21 00 90 45 7f 60 80 45 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 42 35 21 00 90 47 7f 60 80 47 40 00 ff 01 16 20 4e 6f 77 20 79 6f 75 20 6d 75 73 74 20 68 65 61 72 20 43 36 21 00 90 48 7f 60 80 48 40 00 ff 01 0a 54 68 61 6e 6b 20 79 6f 75 21 00 ff 2f 00'.upper())
        if calculated != answer:
            dmp = diff_match_patch()
            patch = dmp.patch_make(calculated.hex(" ").upper(), answer.hex(" ").upper())
            diff = dmp.patch_toText(patch)
            logging.info(diff)

        assert calculated == answer

    def addtrack(self, track, message):
        logging.info(message)
        track.append(message)
        return message.encode(Encoding.MIDI)
