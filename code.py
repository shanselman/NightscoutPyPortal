import time
import board
from adafruit_pyportal import PyPortal

# Set up where we'll be fetching data from
DATA_SOURCE = "https://hanselsugars.azurewebsites.net/api/v1/entries.json?count=1"
BG_VALUE = [0, 'sgv']
BG_DIRECTION = [0, 'direction']

RED = 0xFF0000;
ORANGE = 0xFFA500;
YELLOW = 0xFFFF00;
GREEN = 0x00FF00;

def get_bg_color(val):
    if val > 200:
        return RED
    elif val > 150:
        return YELLOW
    elif val < 60:
        return RED
    elif val < 80:
        return ORANGE
    return GREEN

def text_transform_bg(val):
    return str(val) + ' mg/dl'
    
def text_transform_direction(val):
    if val == "Flat":
        return "→"
    if val == "SingleUp":
        return "↑"
    if val == "DoubleUp":
        return "↑↑"
    if val == "DoubleDown":
        return "↓↓"
    if val == "SingleDown":
        return "↓"
    if val == "FortyFiveDown":
        return "→↓"
    if val == "FortyFiveUp":
        return "→↑"
    return val

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=(BG_VALUE, BG_DIRECTION),
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0xFFFFFF,
                    text_font=cwd+"/fonts/Arial-Bold-24-Complete.bdf",
                    text_position=((90, 120),  # VALUE location
                                   (140, 160)), # DIRECTION location
                    text_color=(0x000000,  # quote text color
                                0x000000), # author text color
                    text_wrap=(35, # characters to wrap for quote
                               0), # no wrap for author
                    text_maxlen=(180, 30), # max text size for quote & author
                    text_transform=(text_transform_bg,text_transform_direction),
                   )

# speed up projects with lots of text by preloading the font!
pyportal.preload_font(b'mg/dl012345789');
pyportal.preload_font((0x2191, 0x2192, 0x2193))
#pyportal.preload_font()

while True:
    try:
        value = pyportal.fetch()
        pyportal.set_background(get_bg_color(value[0]))
        print("Response is", value)
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
    time.sleep(180)
