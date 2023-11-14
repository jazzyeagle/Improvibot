from dotenv import load_dotenv
load_dotenv()

import mido
from mido import Message
import ai

mido.set_backend(name='midojack', load=True)

with mido.open_output() as outport:
    ai.run(outport)
    input('Press [Enter] to quit')
