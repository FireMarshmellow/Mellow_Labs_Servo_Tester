import board
import busio
import digitalio
import rotaryio
import displayio
import terminalio
import time
import pwmio
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
from adafruit_displayio_ssd1306 import SSD1306
from adafruit_motor import servo

# --- Display Setup ---
displayio.release_displays()
i2c = busio.I2C(scl=board.GP9, sda=board.GP8)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 32
display = SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()
display.root_group = splash

# --- PWM & Servo Setup ---
pwm = pwmio.PWMOut(board.GP16, frequency=50)
my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

# --- Inputs Setup ---
button_pins = [board.GP12, board.GP11, board.GP10]
buttons = []
for pin in button_pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.DOWN
    buttons.append(btn)

encoder = rotaryio.IncrementalEncoder(board.GP13, board.GP14)
last_position = encoder.position

encoder_switch = digitalio.DigitalInOut(board.GP15)
encoder_switch.direction = digitalio.Direction.INPUT
encoder_switch.pull = digitalio.Pull.UP  # active low

# --- State Variables ---
current_angle = 90  # Default neutral
step_sizes = [1, 10, 100]
step_index = 0
position1 = None
position2 = None
playback_mode = False
playback_direction = 1
playback_delay = 0.5  # default 0.5 seconds
playback_last_time = 0
going_to_pos2 = True
hold_duration = 1.0  # seconds to hold to save position

button_hold_start = [None, None, None]

# --- Display Elements ---
circle = Circle(10, 16, 10, outline=1, fill=1)
splash.append(circle)

step_label = label.Label(terminalio.FONT, text="1°", x=6, y=20, scale=1)
angle_label = label.Label(terminalio.FONT, text="A:090", x=30, y=5)
mode_label = label.Label(terminalio.FONT, text="M:Man", x=30, y=17)
speed_label = label.Label(terminalio.FONT, text="S:50%", x=30, y=28)

position1_label = label.Label(terminalio.FONT, text="P1", x=90, y=5)
position1_angle_label = label.Label(terminalio.FONT, text="", x=105, y=5)
position2_label = label.Label(terminalio.FONT, text="P2", x=90, y=17)
position2_angle_label = label.Label(terminalio.FONT, text="", x=105, y=17)

splash.append(step_label)
splash.append(angle_label)
splash.append(mode_label)
splash.append(speed_label)
splash.append(position1_label)
splash.append(position1_angle_label)
splash.append(position2_label)
splash.append(position2_angle_label)

# --- Helper Functions ---
def update_servo(angle):
    global current_angle
    angle = max(0, min(180, angle))
    current_angle = angle
    my_servo.angle = angle

def update_display():
    step_label.text = f"{step_sizes[step_index]}°"
    angle_label.text = f"A:{int(current_angle):03}"
    mode_label.text = f"M:{'Ply' if playback_mode else 'Man'}"
    speed_label.text = f"S:{int((1 - playback_delay) * 100)}%"
    position1_angle_label.text = f"{int(position1):03}" if position1 is not None else ""
    position2_angle_label.text = f"{int(position2):03}" if position2 is not None else ""

def change_step_mode():
    global step_index
    step_index = (step_index + 1) % 3

def jump_to_position(pos):
    if pos is not None:
        update_servo(pos)

def save_position(index):
    global position1, position2
    if index == 0:
        position1 = current_angle
    elif index == 2:
        position2 = current_angle

def toggle_playback():
    global playback_mode, playback_last_time
    if position1 is not None and position2 is not None:
        playback_mode = not playback_mode
        playback_last_time = time.monotonic()

def handle_playback():
    global going_to_pos2, playback_last_time
    now = time.monotonic()
    if now - playback_last_time >= playback_delay:
        target = position2 if going_to_pos2 else position1
        update_servo(target)
        going_to_pos2 = not going_to_pos2
        playback_last_time = now

def adjust_speed(delta):
    global playback_delay
    playback_delay -= delta * 0.05
    playback_delay = max(0.05, min(1.0, playback_delay))

# --- Main Loop ---
update_servo(current_angle)
update_display()

while True:
    position = encoder.position
    if position != last_position:
        delta = position - last_position
        last_position = position

        if playback_mode:
            adjust_speed(delta)
        else:
            current_angle += delta * step_sizes[step_index]
            current_angle = max(0, min(180, current_angle))
            update_servo(current_angle)

        update_display()

    if not encoder_switch.value:
        time.sleep(0.2)
        while not encoder_switch.value:
            pass
        change_step_mode()
        update_display()

    now = time.monotonic()
    for i, button in enumerate(buttons):
        if button.value:
            if button_hold_start[i] is None:
                button_hold_start[i] = now
        else:
            if button_hold_start[i] is not None:
                held_time = now - button_hold_start[i]
                button_hold_start[i] = None
                if held_time >= hold_duration:
                    save_position(i)
                else:
                    if i == 0:
                        jump_to_position(position1)
                    elif i == 1:
                        toggle_playback()
                    elif i == 2:
                        jump_to_position(position2)
                update_display()

    if playback_mode:
        handle_playback()

    time.sleep(0.05)

