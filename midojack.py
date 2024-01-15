# midojack.py
#
# This file defines the JACK Backend for Mido.

import os
import jack
import mido
from mido import Message, tick2second
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
        print('_open')
        outbound_message_queue = {}
        self.current_frame = 0
        for output_port in os.environ['JACK_MIDI_OUTPUT_PORTS'].split('|'):
            client.midi_outports.register(output_port)
        for curr_output in client.midi_outports:
            print(curr_output.name)
        client.set_process_callback(self.process)
        client.activate()

    def _close(self, **kwargs):
        print('_close')
        #for outport in client.midi_outports:
        #    outport._send(Message('control_change', control=123, value=0))
        #mido.ports.reset_messages()
        client.deactivate()
        client.close()

    def process(self, nframes):
        #print(f'process: {len(list(outbound_message_queue.keys()))}')
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
        print(f'time: {message.dict()["time"]}, samplerate: {client.samplerate}')
        new_time = int((message.dict()['time'] / 480) * client.samplerate)
        #new_time = int((message.dict()['time'] / 120) * client.samplerate)
        #new_time = int(message.dict()['time'])
        stored_time = current_time + new_time
        print(f'new_time: {new_time}, stored_time: {stored_time}')
        if stored_time not in outbound_message_queue:
            outbound_message_queue[stored_time] = []
            
        outbound_message_queue[stored_time].append(message.copy(time=new_time))
