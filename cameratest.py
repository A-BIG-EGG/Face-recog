import cv2
import sys
import os
import logging as log
import datetime as dt
from time import sleep
from lib.ms_cognitive_imagerec import ms_WhatDoYouSee, ms_WhoDoYouSee, ms_GetFaceAttribs, FaceAttribs
from PIL import Image
import requests
from picamera import PiCamera
import time

camera = PiCamera() #Define camera (won't work on non-pi devices)
camera.vflip = True #Rotate image by flipping v and h
camera.hflip = True
time.sleep(1)

camera.capture("img.jpg") #Save image as .jpg

body = open('img.jpg','rb').read() #Read image in API call-firendly format

try:
    response = ms_WhoDoYouSee(body) #Call API- see ms_cognitive_imagerec for details and options
    print("RESPONSE:" + str(response.json())) #Prints json response to the console

except Exception as e:
    print(e)

os.remove("img.jpg")
