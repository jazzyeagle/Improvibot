#song.py

# This file defines the song class

from enum import Enum
import mido
from mido import Message, MetaMessage, MidiFile, MidiTrack
from midojack import client

mido.set_backend(name='midojack', load=True)

# Denotes the root MIDI note value based on Middle C (C4) = 60.
class Key(Enum):
    A       = 57
    A_Sharp = 58
    B_Flat  = 58
    B       = 59
    C       = 60
    C_Sharp = 61
    D_Flat  = 61
    D       = 62
    D_Sharp = 63
    E_Flat  = 63
    E       = 64
    F       = 65
    F_Sharp = 66
    G_Flat  = 66
    G       = 67
    G_Sharp = 68
    A_Flat  = 69

def key_name(k):
    match k:
        case Key.A:
            return 'A'
        case Key.A_Sharp:
            return 'A#'
        case Key.B_Flat:
            return 'Bb'
        case Key.B:
            return 'B'
        case Key.C:
            return 'C'
        case Key.C_Sharp:
            return 'C#'
        case Key.D_Flat:
            return 'Db'
        case Key.D:
            return 'D'
        case Key.D_Sharp:
            return 'D#'
        case Key.E_Flat:
            return 'Eb'
        case Key.E:
            return 'E'
        case Key.F:
            return 'F'
        case Key.F_Sharp:
            return 'F#'
        case Key.G_Flat:
            return 'Gb'
        case Key.G:
            return 'G'
        case Key.G_Sharp:
            return 'G#'
        case Key.A_Flat:
            return 'Ab'

class Mode(Enum):
    Major = [ 0.20, 0.01, 0.05, 0.01, 0.20, 0.20, 0.01, 0.20, 0.01, 0.05, 0.01, 0.05 ]
    Minor = [ 0.20, 0.01, 0.05, 0.20, 0.01, 0.20, 0.01, 0.20, 0.01, 0.05, 0.01, 0.05 ]

NOTE_LENGTHS = [0.25,   # 16th Note
                0.5,    # 8th  Note
                1.0,    # Quarter Note
                2.0,    # Half Note
                4.0]    # Whole Note

class Song(MidiFile):
    def __init__(self, key=Key.C, mode=Mode.Major, bpm=120, beats_per_bar=4, beat_note=4):
        super().__init__(type=0)
        self.key   = key
        self.mode  = mode
        self.bpm   = bpm
        self.bpb   = beats_per_bar
        self.nb    = beat_note
        self.tempo = mido.bpm2tempo(self.bpm, time_signature=(self.bpb, self.nb))

    def add_instrument(self, name='instrument 1'):
        #track = self.add_track(name)
        track = MidiTrack()
        track.name = name
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.bpm, time_signature=(self.bpb, self.nb))))
        track.append(MetaMessage('time_signature', numerator=self.bpb, denominator=self.nb))
        track.append(MetaMessage('key_signature', key=key_name(self.key)))
        #TODO: mode is not an option.  In order to store all data about what was used to generate each song,
        #      custom meta messages may need to be generated.  See https://mido.readthedocs.io/en/latest/meta_message_types.html?highlight=MetaMessage#implementing-new-or-custom-meta-messages
        return track

    def jackplay(self, outport):
        print(f'\t# Tracks:    {len(self.tracks)}')
        print(f'\tsong length: {self.length}\n')
        #self.print_tracks()
        for msg in self.tracks[0]:
        #for msg in self.play():
            if (not msg.is_meta):
                message = msg.copy()
                # Convert the timestamp so the midojack module can convert to samplerate
                #if msg.time==0:
                #    message = msg.copy()
                #else:
                #    message = msg.copy(time=self.tempo2bpm(msg.time))
                outport._send(message)

    #def save(self, filename):
    #    self.save(filename)

    def make_note(self, track, note_float, velocity_float, length_float):
        note = int(note_float)
        velocity = int(velocity_float)
        length = self.note_length_ticks(length_float)

        print(f'Note: {note}\tVelocity: {velocity}\tLength: {length}\n')
        track.append(Message('note_on',  note=note, velocity=velocity))
        track.append(Message('note_off', note=note, velocity=velocity, time=length))
    
    def note_length_tempo(self, value):
        return int(self.tempo * value)

    def note_length_bpm(self, value):
        return int(self.bpm * value)

    def note_length_ticks(self, value):
        return int(self.ticks_per_beat * value)
    
    def tempo2bpm(self, value):
        print(f'value={value}, time_signature = {self.bpb}/{self.nb}, new_value: {int(mido.tempo2bpm(value, time_signature=(self.bpb, self.nb)))}')
        return int(mido.tempo2bpm(value, time_signature=(self.bpb, self.nb)))
