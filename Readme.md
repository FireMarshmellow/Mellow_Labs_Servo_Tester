# DIY Servo Tester using Raspberry Pi Pico and CircuitPython

This repository provides all the necessary files to create your own DIY servo tester using a Raspberry Pi Pico running CircuitPython. The project allows you to quickly and precisely test servo motors with ease, using a rotary encoder for accurate adjustments and an OLED display for clear feedback.

## Project video
[![Video Title](https://img.youtube.com/vi/ikiF_kmtoJc/0.jpg)](https://www.youtube.com/watch?v=ikiF_kmtoJc)

## Features
- **Rotary Encoder Control**: Easily adjust servo position in steps of 1°, 10°, or 100°.
- **OLED Display**: Clearly displays current servo angle, step size, and operational mode.
- **Automated Movement**: Set two positions and let the servo automatically cycle between them, adjustable speed included.
- **Easy Setup**: Simply upload provided files to your Raspberry Pi Pico and you're ready to go.

## Hardware Requirements
- Raspberry Pi Pico (W or standard)
- Rotary Encoder (with pushbutton)
- SSD1306 OLED Display
- Servo motor
- Three push buttons
- Jumper wires and breadboard

## Software Requirements
- CircuitPython installed on Raspberry Pi Pico

## Installation

1. Ensure your Raspberry Pi Pico has CircuitPython installed. ([CircuitPython Installation Guide](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython))

2. Clone or download this repository.

3. Copy the following files to the root of your Raspberry Pi Pico:
   - `code.py`
   - Entire `lib` directory (contains necessary CircuitPython libraries)

Your Pico filesystem should look like:
```
/
├── code.py
└── lib/
    └── (required library files)
```

4. Connect hardware components as shown in the project video or described in the comments of `code.py`.

5. Power up the Pico and enjoy testing your servo motors!

## Usage
- Turn the rotary encoder to adjust servo angle.
- Press rotary encoder button to switch between step sizes (1°, 10°, 100°).
- Button 1 saves current position as Position 1.
- Button 3 saves current position as Position 2.
- Button 2 toggles automated movement between Position 1 and Position 2.
- During automated playback, rotate encoder to adjust servo movement speed.

## License

This project is open-source and available under the [MIT License](LICENSE). Feel free to use, modify, and distribute it!