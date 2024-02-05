import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from PIL import Image, ImageDraw

# Define the figures (8x8 matrices)
figures = [
    [
        0b00000000,
        0b01100110,
        0b11111111,
        0b11111111,
        0b01111110,
        0b00111100,
        0b00011000,
        0b00000000,
    ],
    [
        0b11111111,
        0b10111101,
        0b10011001,
        0b11111111,
        0b11011011,
        0b10000001,
        0b11100111,
        0b11111111,
    ],
    [
        0b11111111,
        0b01111110,
        0b00111100,
        0b00011000,
        0b00011000,
        0b00111100,
        0b01111110,
        0b11111111,
    ],
    [
        0b00111100,
        0b01000010,
        0b10100101,
        0b10000001,
        0b10100101,
        0b10011001,
        0b01000010,
        0b00111100,
    ],
    [
        0b11111111,
        0b10011001,
        0b10011001,
        0b11111111,
        0b11100111,
        0b11000011,
        0b11011011,
        0b11111111,
    ]
]

# Set up the MAX7219 LED matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0)

# Function to display a figure on the LED matrix
def display_figure(figure):
    image = Image.new("1", (8, 8), "black")
    draw = ImageDraw.Draw(image)

    for row in range(8):
        for col in range(8):
            pixel_value = (figure[row] >> (7 - col)) & 1
            draw.point((col, row), fill="white" if pixel_value else "black")

    device.display(image)

# Main program
try:
    for figure in figures:
        display_figure(figure)
        time.sleep(3)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    pass

finally:
    # Clear the display before exiting
    device.clear()