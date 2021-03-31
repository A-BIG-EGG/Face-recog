import cv2
import sys
import os
import logging as log
import datetime as dt
from time import sleep
from lib.ms_cognitive_imagerec import ms_WhatDoYouSee, ms_WhoDoYouSee, ms_GetFaceAttribs, FaceAttribs
from PIL import Image,ImageDraw,ImageFont
import requests
from picamera import PiCamera
from waveshare_epd import epd2in13_V2
import traceback
picdir = 'pic'
libdir = 'lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
camera = PiCamera() #Define camera (won't work on non-pi devices)
camera.vflip = True #Rotate image by flipping v and h
camera.hflip = True

#Alert user to image being taken
epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)
image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(image)
draw.text((35, 45), 'Ready?', font = font40, fill = 0)
image = image.transpose(Image.ROTATE_180) #rotates image?
epd.display(epd.getbuffer(image))
time.sleep(1)

camera.capture("img.jpg") #Save image as .jpg

body = open('img.jpg','rb').read() #Read image in API call-firendly format

try:
    response = ms_WhoDoYouSee(body) #Call API- see ms_cognitive_imagerec for details and options
    print("RESPONSE:" + str(response.json())) #Prints json response to the console

except Exception as e:
    print(e)

os.remove("img.jpg")
