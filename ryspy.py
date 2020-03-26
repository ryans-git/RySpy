import time, re
from signal import signal, SIGINT
from sys import exit
from PCA9685 import Servo

TILT_CHAN = 0
PAN_CHAN  = 1
PT_SERVOS  = []

# Add a read command instead of global
CURR_PAN  = 90
CURR_TILT = 90

# Servo move speed in miliseconds
SERVO_MAX    = 0
SERVO_FAST   = 1
SERVO_NORMAL = 5
SERVO_SLOW   = 100
SERVO_CRAWL  = 500

def main():
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
d  -> Demo
h  -> Home (90,90)
q  -> quit
""")
        pattern = re.compile("^(p(l|r|[0-9]{1,3})|t(d|u|[0-9]{1,3})|d|h)$")
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
            elif move == "d":
                lap(SERVO_FAST)
            elif move == "h":
                set_pan(90, SERVO_FAST)
                set_tilt(90, SERVO_NORMAL)
        else:
            print("Invalid selection.")
    
        print("deg:   " + str(deg))
        print("PAN:   " + str(CURR_PAN))
        print("TILT:  " + str(CURR_TILT))

######################################################
# Pan Functions
def set_pan(degree, speed=SERVO_MAX):
    if valid_degree(degree):
        global CURR_PAN 
        if speed == SERVO_MAX:
            PT_SERVOS[PAN_CHAN].write(degree)
        else:
            direction = 1 if CURR_PAN < degree else -1
            for deg in range(CURR_PAN, degree, direction):
                PT_SERVOS[PAN_CHAN].write(deg) 
                time.sleep(speed / 100.0)
        CURR_PAN = degree

def pan_left(add_degree=5):
    set_pan(CURR_PAN + add_degree)

def pan_right(sub_degree=5):
    set_pan(CURR_PAN - sub_degree)

######################################################
# Tilt Functions
def set_tilt(degree, speed=SERVO_MAX):
    if valid_degree(degree):
        global CURR_TILT 
        if speed == SERVO_MAX:
            PT_SERVOS[TILT_CHAN].write(degree)
        else:
            direction = 1 if CURR_TILT < degree else -1
            for deg in range(CURR_TILT, degree, direction):
                PT_SERVOS[TILT_CHAN].write(deg)
                time.sleep(speed / 100.0)
        CURR_TILT = degree

def tilt_up(add_degree=5):
    set_tilt(CURR_TILT + add_degree)

def tilt_down(sub_degree=5):
    set_tilt(CURR_TILT - sub_degree)

######################################################
# Demos
def lap(speed):
    '''
    Sent Pan-Tilt on a loop to max/min angles
    Args:
        Int: milisecond delay between moves
    TODO:
        Validate speed arg
    '''
    global CURR_PAN
    global CURR_TILT
    CURR_PAN = CURR_TILT = 0

    set_pan(CURR_PAN)
    set_tilt(CURR_TILT)

    print("Demo Start")
    print("PAN:   " + str(CURR_PAN))
    print("TILT:  " + str(CURR_TILT))

    for deg in range(0,180,5):
        set_tilt(deg, speed)
        set_pan(deg, speed)
    
    print("Moved 180")
    print("PAN:   " + str(CURR_PAN))
    print("TILT:  " + str(CURR_TILT))
    
    for deg in range(180,0,-5):
        set_tilt(deg, speed)
        set_pan(deg, speed)
    
    print("Move to 0")
    print("PAN:   " + str(CURR_PAN))
    print("TILT:  " + str(CURR_TILT))

    # Go back home
    for deg in range(0,90,5):
        set_tilt(deg, speed)
        set_pan(deg, speed)

    print("Moved home")
    print("PAN:   " + str(CURR_PAN))
    print("TILT:  " + str(CURR_TILT))


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
    set_pan(90)
    set_tilt(90)
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

if __name__ == "__main__":
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    PT_SERVOS.append(Servo.Servo(TILT_CHAN))
    PT_SERVOS.append(Servo.Servo(PAN_CHAN))
    Servo.Servo(TILT_CHAN).setup()
    Servo.Servo(PAN_CHAN).setup()

    set_pan(CURR_PAN, SERVO_FAST)
    set_tilt(CURR_TILT, SERVO_FAST)

    main()