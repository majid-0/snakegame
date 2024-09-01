from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

# Create a sine wave burst that could mimic a bite sound
frequency = 500  # Frequency in Hz
duration = 50    # Duration in milliseconds

# Generate the bite sound using a sine wave
sine_wave = Sine(frequency).to_audio_segment(duration=duration)

# Correcting the white noise generation by converting frame count to an integer
noise = AudioSegment(
    np.random.normal(0, 1, int(sine_wave.frame_count())).astype(np.int16).tobytes(),
    frame_rate=sine_wave.frame_rate,
    sample_width=sine_wave.sample_width,
    channels=sine_wave.channels
)
bite_sound = sine_wave.overlay(noise - 20)

# Export the sound as 'bite.wav'
bite_sound.export("bite.wav", format="wav")
