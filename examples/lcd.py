import socket
import st7735  # Use the lowercase module name as per the deprecation warning
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
import time

# Add delay to ensure that Wi-Fi is connected before displaying IP
time.sleep(0)

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""ipconfig.py - Display IP address example on the 0.96" LCD.
Press Ctrl+C to exit!
""")

# Create LCD class instance.
disp = st7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display.
disp.begin()

# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height

# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Text settings.
font_size = 25
font = ImageFont.truetype(UserFont, font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 170)

# Get IP address.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
message = s.getsockname()[0]
print(message)
s.close()

# Calculate text size and position.
bbox = draw.textbbox((0, 0), message, font=font)
size_x, size_y = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (WIDTH - size_x) / 2
y = (HEIGHT / 2) - (size_y / 2)

# Draw background rectangle and write text.
draw.rectangle((0, 0, 160, 80), back_colour)
draw.text((x, y), message, font=font, fill=text_colour)
disp.display(img)

# Keep running.
try:
    while True:
        pass

# Turn off backlight on control-c
except KeyboardInterrupt:
    disp.set_backlight(0)
