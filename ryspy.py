import time, re
from signal import signal, SIGINT
from sys import exit
from PCA9685 import Servo

TILT_CHAN = 0
PAN_CHAN  = 1
PI_SERVO  = []

# Add a read command instead of global
CURR_PAN  = 90
CURR_TILT = 90

######################################################
# Pan Functions
def set_pan(degree):
    if valid_degree(degree):
        PI_SERVO[PAN_CHAN].write(degree)
        CURR_PAN = degree

def pan_left(add_degree=5):
    set_pan(CURR_PAN + add_degree)

def pan_right(sub_degree=5):
    set_pan(CURR_PAN - sub_degree)

######################################################
# Tilt Functions
def set_tilt(degree):
    if valid_degree(degree):
        PI_SERVO[TILT_CHAN].write(degree)
        CURR_TILT = degree

def tilt_up(add_degree=5):
    set_tilt(CURR_TILT + add_degree)

def tilt_down(sub_degree=5):
    set_tilt(CURR_TILT - sub_degree)

######################################################
# Helpers
def valid_degree(degree):
    try:
        if not isinstance(degree, int):
            raise TypeError("Invalid degree type. Type: " + type(degree) + " must be type int")
        if degree < 0 or degree > 180:
            raise ValueError("Degree must be in boundry > 0 && < 180. Given: " + str(degree))
    except (ValueError, TypeError) as err:
        print(err)
        return False
    return True

def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

if __name__ == "__main__":
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    PI_SERVO.append(Servo.Servo(TILT_CHAN))
    PI_SERVO.append(Servo.Servo(PAN_CHAN))
    Servo.Servo(TILT_CHAN).setup()
    Servo.Servo(PAN_CHAN).setup()

    set_pan(CURR_PAN)
    set_tilt(CURR_TILT)

    while True:
        print("""
Move Pan-Tilt
----------------
pl -> Left pan
pr -> Right pan
pX -> Pan X degrees
tu -> Up tilt
td -> Down tilt
tX -> Tile X degrees
q  -> quit
""")
        pattern = re.compile("^(p(l|r|[0-9]{1,3})|t(d|u|[0-9]{1,3}))$")
        move = raw_input("-> ")
        if move == "q":
            exit(0)
        if re.match(pattern, str(move)) is not None:
            if move == "pl":
                pan_left()
            elif move == "pr":
                pan_right()
            elif move == "pr":
                pan_right()
            elif re.match(re.compile("^p[0-9]{1,3}$"),move):
                deg = int(re.search(r'\d+', move).group())
                set_pan(deg)
            elif move == "tu":
                tilt_up()
            elif move == "td":
                tilt_down()
            elif re.match(re.compile("^t[0-9]{1,3}$"),move):
                deg = int(re.search(r'\d+', move).group())
                set_tilt(deg)
        else:
            print("Invalid selection.")
