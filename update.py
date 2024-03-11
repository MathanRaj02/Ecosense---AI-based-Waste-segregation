from keras.models import load_model
import cv2
from gtts import gTTS
import os
import numpy as np
import pyfirmata
import pygame
import time

#port defining
PORT = 'COM5'
board = pyfirmata.Arduino(PORT)
servo_pin = board.get_pin('d:9:s')

# Initialize pygame mixer
pygame.mixer.init()

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Time duration for each image recognition session (in seconds)
    recognition_duration = 10
    start_time = time.time()

    # Lists to store predictions during the recognition period
    predictions = []
    confidence_scores = []

    while (time.time() - start_time) < recognition_duration:
        # Grab the webcam's image.
        ret, image = camera.read()

        # Resize the raw image into (224-height, 224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Make the image a numpy array and reshape it to the model's input shape.
        image_copy = image.copy()  # Make a copy for annotation
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predict the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Store predictions and confidence scores
        predictions.append(class_name[2:])
        confidence_scores.append(confidence_score)

        # Draw a rectangle around the detected object
        cv2.rectangle(image_copy, (0, 0), (224, 224), (0, 255, 0), 2)  # Green rectangle

        # Show the image with the rectangle in a new window
        cv2.imshow("Annotated Image", image_copy)

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

    # Find the category with the highest average confidence score for the session
    if predictions:
        avg_confidences = np.mean(confidence_scores)
        max_confidence_index = np.argmax(avg_confidences)
        predicted_category = predictions[max_confidence_index]

        # Print the predicted category and assign numbers based on conditions
        if "recyclable" in predicted_category.lower():
            category_number = 1
            servo_pin.write(180)
            time.sleep(3)  # Wait for 3 seconds at 60 degrees
            servo_pin.write(0)  # Return to 0 degrees
            audio_file = "it-s recyclable 1.wav"
            pygame.mixer.music.load(audio_file)

            # Play the audio
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        elif "non-recyclable" in predicted_category.lower():
            category_number = 2
            servo_pin.write(180)
            time.sleep(3)  # Wait for 3 seconds at 60 degrees
            servo_pin.write(0)  # Return to 0 degrees
            audio_file = "oh thats non rec 1.wav"
            pygame.mixer.music.load(audio_file)

            # Play the audio
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        elif "hazardous" in predicted_category.lower():
            category_number = 3
            servo_pin.write(180)
            time.sleep(3)  # Wait for 3 seconds at 60 degrees
            servo_pin.write(0)  # Return to 0 degrees
            audio_file = "oh no it-s Hazar 2.wav"
            pygame.mixer.music.load(audio_file)

            # Play the audio
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        elif "organic" in predicted_category.lower():
            category_number = 4
            servo_pin.write(180)
            time.sleep(3)  # Wait for 3 seconds at 60 degrees
            servo_pin.write(0)  # Return to 0 degrees
            audio_file = "it-s organic yo 3.wav"
            pygame.mixer.music.load(audio_file)

            # Play the audio
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            category_number = 0  # Default to 0 if category not recognized

        print("Predicted Category:", predicted_category)
        print("Category Number:", category_number)

    # Ask the user if they want to continue or quit
    print("Press 'q' to quit or any other key to continue...")
    quit_key = cv2.waitKey(0)

    # 113 is the ASCII code for 'q' key
    if quit_key == 113:
        board.exit()
        break


cv2.destroyAllWindows()
camera.release()
