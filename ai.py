import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import mido
from mido import MidiFile, MidiTrack, Message
from midojack import make_note

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

NUM_NOTES = 10
NOTE_VALUES = 128
VELOCITY_VALUES = 128
NOTE_LENGTHS = [0.25, 0.5, 1.0, 2.0, 4.0]
FEEDBACK_VALUES = [1, 2, 3, 4, 5]
epochs = 1000


def generate_initial_sequence(num_notes):
    return {
        'note': np.random.randint(0, NOTE_VALUES, num_notes),
        'velocity': np.random.randint(0, VELOCITY_VALUES, num_notes),
        'length': np.random.choice(NOTE_LENGTHS, num_notes)
    }

model = Sequential([
    LSTM(128, input_shape=(NUM_NOTES, 3)),
    Dense(64, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='mse')


def generate_midi(outport, model_output):
    # Convert model output to MIDI messages
    midi_track = MidiTrack()
    print(model_output)
    #for output in model_output[0]:
    #    print(output)
    #    msg = Message('note_on', note=output[0], velocity=output[1])
    #    midi_track.append(msg)
    #    msg = Message('note_off', note=output[0], velocity=0)
    #    midi_track.append(msg)
    for note, velocity, length in model_output:
        make_note(outport, note, velocity, length)


def get_user_feedback():
        # Simulated function to get user feedback
            return np.random.choice(FEEDBACK_VALUES)

def train_model(model, input_sequence, feedback):
    target_output = np.array([input_sequence])  # Target output is the same as input for now

    # Adjust target output based on feedback
    feedback_factor = feedback / 5.0  # Normalize feedback to a factor between 0 and 1
    target_output[:, :, :2] *= feedback_factor  # Adjust note and velocity based on feedback
    target_output[:, :, 2] *= 1.0 / feedback_factor  # Adjust note length inversely based on feedback

    model.fit(input_sequence[np.newaxis, :, :], target_output, epochs=1, verbose=0)

def run(outport):
    for epoch in range(epochs):
        input_sequence = generate_initial_sequence(NUM_NOTES)
        input_sequence = np.array([
            input_sequence['note'],
            input_sequence['velocity'],
            input_sequence['length']
        ]).T  # Transpose to have shape (num_notes, 3)
        model_output = model.predict(np.array([input_sequence]))
        user_feedback = get_user_feedback()
        generate_midi(outport, model_output)
        train_model(model, input_sequence, user_feedback)
