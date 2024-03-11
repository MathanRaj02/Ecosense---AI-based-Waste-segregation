from keras.models import load_model
import cv2
import numpy as np
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(1)

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

        # Show the image in a window
        cv2.imshow("Webcam Image", image)

        # Make the image a numpy array and reshape it to the model's input shape.
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

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

    # Find the category with the highest average confidence score for the session
    if predictions:
        avg_confidences = np.mean(confidence_scores)
        max_confidence_index = np.argmax(avg_confidences)
        print("Category with the highest average confidence score:", predictions[max_confidence_index])

    # Ask the user if they want to continue or quit
    print("Press 'q' to quit or any other key to continue...")
    quit_key = cv2.waitKey(0)

    # 113 is the ASCII code for 'q' key
    if quit_key == 113:
        break

cv2.destroyAllWindows()
camera.release()
