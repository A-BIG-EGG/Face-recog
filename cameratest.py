import cv2
import sys
import os
import logging as log
import datetime as dt
import time
from lib.ms_cognitive_imagerec import ms_WhatDoYouSee, ms_WhoDoYouSee, ms_GetFaceAttribs, FaceAttribs
from PIL import Image,ImageDraw,ImageFont
import requests
from picamera import PiCamera
picdir = 'pic'
libdir = 'lib'
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd2in13_V2
import traceback

epd = epd2in13_V2.EPD()
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
time_image = Image.new('1', (epd.height, epd.width), 255)
time_draw = ImageDraw.Draw(time_image)
epd.init(epd.FULL_UPDATE)
epd.displayPartBaseImage(epd.getbuffer(time_image))

camera = PiCamera() #Define camera (won't work on non-pi devices)
camera.vflip = True #Rotate image by flipping v and h
camera.hflip = True

#Alert user to image being taken
# epd.init(epd.FULL_UPDATE)
# epd.Clear(0xFF)
epd.init(epd.PART_UPDATE)
time_draw.rectangle((120, 80, 220, 105), fill = 255)
time_draw.text((15, 35), '3', font = font60, fill = 0)
epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
time_draw.rectangle((120, 80, 220, 105), fill = 255)
time_draw.text((95, 35), '2', font = font60, fill = 0)
epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
time_draw.rectangle((120, 80, 220, 105), fill = 255)
time_draw.text((175, 35), '1', font = font60, fill = 0)
epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
time.sleep(1)

camera.capture("img.jpg") #Save image as .jpg
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)

body = open('img.jpg','rb').read() #Read image in API call-firendly format

try:
    response = ms_WhoDoYouSee(body) #Call API- see ms_cognitive_imagerec for details and options
    print("RESPONSE:" + str(response.json())) #Prints json response to the console

except Exception as e:
    print(e)

os.remove("img.jpg")
