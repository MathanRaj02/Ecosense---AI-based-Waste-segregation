import pyfirmata
import time

# Define the COM port (Arduino USB port) you are using. Update this with your port.
PORT = 'COM5'  # Update this with your Arduino's port

# Create a new board object
board = pyfirmata.Arduino(PORT)

# Define the pin to which the servo is connected (pin 9)
servo_pin = board.get_pin('d:9:s')  # Set pin 9 as a servo

# Function to set the servo angle
def set_servo_angle(angle):
    if 0 <= angle <= 180:
        servo_pin.write(angle)
        time.sleep(0.1)  # Optional delay to allow the servo to reach the target angle
    else:
        print("Angle should be between 0 and 180 degrees.")

try:
    while True:
        # Prompt the user for the desired angle
        user_input = input("Enter the angle (0-180) or 'q' to quit: ")

        if user_input.lower() == 'q':
            break

        angle = int(user_input)
        set_servo_angle(angle)

except KeyboardInterrupt:
    pass

# Close the board connection when done
board.exit()
