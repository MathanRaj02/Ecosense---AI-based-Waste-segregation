import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the MP3 audio file (replace 'your_audio.mp3' with the actual file path)
audio_file = "oh thats non rec 1.wav"
pygame.mixer.music.load(audio_file)

# Play the audio
pygame.mixer.music.play()

# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
