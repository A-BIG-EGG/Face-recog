import sys
import os
picdir = 'pic'
libdir = 'lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V2 Demo")

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    logging.info("Initialising font definitions")
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
    logging.info("Fonts defined")

    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    draw.text((35, 45), 'I <3 Angel', font = font40, fill = 0)
    image = image.transpose(Image.ROTATE_180) #rotates image?
    epd.display(epd.getbuffer(image))
    time.sleep(2)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
