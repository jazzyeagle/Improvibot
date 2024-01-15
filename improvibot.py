from dotenv import load_dotenv
load_dotenv()

import mido
from mido import Message
import ai

mido.set_backend(name='midojack', load=True)

with mido.open_output(autoreset=True) as outport:
    cont = True
    while cont:
        song = ai.generate_song(outport)
        print('Press [Enter] to generate a new song, "quit" to quit.')
        response = input()
        if response == 'quit':
            cont= False
            outport.panic()
