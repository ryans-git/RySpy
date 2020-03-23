import time
from SunFounder_PCA9685 import Servo

TILT_CHAN = 0
PAN_CHAN = 1
PI_SERVO = []

# Add a read command instead of global


def set_pan(degree):
    if degree < 0 or degree > 180:
        raise ValueError("Degree must be in boundry > 0 && < 180")

    PI_SERVO[PAN_CHAN].write(degree)

def pan_left(degree=5):
    print()


if __name__ == "__main__":
    PI_SERVO.append(Servo.Servo(TILT_CHAN))
    PI_SERVO.append(Servo.Servo(PAN_CHAN))

    while True:
        x = input("Enter Degree: ")
        set_pan(x)
