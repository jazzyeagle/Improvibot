# midojack.py
#
# This file defines the JACK Backend for Mido.

import os
import jack
from mido import Message
from mido.ports import BaseOutput

client = jack.Client(os.environ['JACK_NAME'])
outbound_message_queue = {}
NOTE_LENGTHS = [0.25, 0.5, 1.0, 2.0, 4.0]


def get_devices():
    devices = []
    input_names  = set(client.get_ports(is_audio=False, is_output=False))
    output_names = set(client.get_ports(is_audio=False, is_output=True))
                
    for name in sorted(input_names | output_names):
        devices.append({
            'name':      name,
            'is_input':  name in input_names,
            'is_output': name in output_names,
            })
    return devices

class Output(BaseOutput):
    def _open(self, **kwargs):
        outbound_message_queue = {}
        self.current_frame = 0
        for output_port in os.environ['JACK_MIDI_OUTPUT_PORTS'].split('|'):
            client.midi_outports.register(output_port)
        for curr_output in client.midi_outports:
            print(curr_output.name)
        client.set_process_callback(self.process)
        client.activate()

    def _close(self, **kwargs):
        client.deactivate()
        client.close()

    def process(self, nframes):
        if len(list(outbound_message_queue.keys())) > 0:
            for curr_output in client.midi_outports:
                curr_output.clear_buffer()
            for curr_frame in range(self.current_frame, self.current_frame + nframes):
                if curr_frame in outbound_message_queue:
                    for curr_output in client.midi_outports:
                        curr_output.clear_buffer()
                        for message in outbound_message_queue[curr_frame]:
                            curr_output.write_midi_event(curr_frame - self.current_frame, message.bytes())
            latest_time = list(outbound_message_queue.keys())[-1]
            self.current_frame += nframes
            if self.current_frame > latest_time:
                self.current_frame = 0

    def _send(self, message):
        if len(outbound_message_queue.keys()) > 0:
            current_time = next(reversed(outbound_message_queue.keys()))
        else:
            current_time = 0
        new_time = current_time + message.time
        if new_time not in outbound_message_queue:
            outbound_message_queue[new_time] = []
            
        outbound_message_queue[new_time].append(message.copy())

def make_note(outport, note_float, velocity_float, length_float):
    note = float_to_int(note_float)
    velocity = float_to_int(velocity_float)
    length = float_to_length(length_float)
    print(f'Note: {note}\tVelocity: {velocity}\tLength: {length}\n')
    outport._send(Message('note_on',  note=note, velocity=velocity))
    outport._send(Message('note_off', note=note, velocity=velocity, time=length))

# Converts a floating point number to an int in the range of 0 - 127
# Negative numbers will be 0 - 64, Positive 65 - 127
def float_to_int(value):
    return int(value * 128)
    #if value < 0:
    #    offset = 0
    #else:
    #    offset = 64
    #return int(abs(value) * 31) + offset

# TODO: Current logic assumes client.samplerate = 1 quarter note
#       Need to adjust to account for BPM in the future
def float_to_length(value):
    length_index = int(value * 6)
    #length_index = int((abs(value) - int(abs(value))) * 6)
    print(f'\tlength_index: {length_index}')
    return int(NOTE_LENGTHS[length_index] * client.samplerate)
