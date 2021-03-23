#!/usr/bin/python
# -*- coding:utf-8 -*-
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
    font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)

    logging.info("Fonts defined")
    # # partial update
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))

    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):
        time_draw.rectangle((30, 40, 220, 105), fill = 255)
        time_draw.text((30, 40), time.strftime('%H:%M:%S'), font = font48, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
        num = num + 1
        if(num == -1):
            break
    # epd.Clear(0xFF)
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
