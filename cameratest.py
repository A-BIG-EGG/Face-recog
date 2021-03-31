import cv2
import sys
import os
import logging as log
import time
import textwrap
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

#Define face detection cascades
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#Set up e-paper display with font definitions etc
epd = epd2in13_V2.EPD()
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)


camera = PiCamera() #Define camera (won't work on non-pi devices)
camera.vflip = True #Rotate image by flipping v and h
camera.hflip = True
n = 0

while True:
    #Alert user to image being taken with a 3,2,1 countdown, partially refreshed
    #Rotation must be there because the screen is upside down lol
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    epd.init(epd.PART_UPDATE)
    time_draw.rectangle((120, 80, 220, 105), fill = 255)
    time_draw.text((15, 35), '3', font = font60, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
    time_draw.rectangle((120, 80, 220, 105), fill = 255)
    time_draw.text((95, 35), '2', font = font60, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
    time_draw.rectangle((120, 80, 220, 105), fill = 255)
    time_draw.text((185, 35), '1', font = font60, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
    time.sleep(1)

    camera.capture("img.jpg") #Save current camera frame as img.jpg
    epd.init(epd.FULL_UPDATE) #Clear the display to prevent ghosting
    epd.Clear(0xFF)

    #Check image for faces
    img = cv2.imread("img.jpg")
    faces = faceCascade.detectMultiScale(
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    print('Number of faces: '+str(len(faces)))

    if len(faces) > 0: #Action if there are faces in the frame
        body = open('img.jpg','rb').read() #Read image in API call-firendly format
        try:
            response = ms_WhoDoYouSee(body) #Call API- see ms_cognitive_imagerec for details and options
            for face in response:
                n += 1
                faceAttribs = ms_GetFaceAttribs (face)
            if faceAttribs.glasses == 'NoGlasses':
                glasses_txt = ""
            else:
                glasses_txt = "%s is wearing %s"% (faceAttribs.gender_noun, faceAttribs.glasses)

            top_emotion_txt = "%s top emotion is %s at %2.f %% confidence"% (faceAttribs.gender_possessive, faceAttribs.top_emotion, faceAttribs.top_emotion_conf)

            iSeeText = "I see a %s age %d %s, %s"% (faceAttribs.gender, faceAttribs.age, top_emotion_txt, glasses_txt) #Build sentence describing the results
            iSeeText = textwrap.fill(iSeeText,26) #Wrap the text for future display
            image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(image)
            draw.text((10, 20), iSeeText, font = font20, fill = 0)
            image = image.transpose(Image.ROTATE_180) #rotates image
            epd.display(epd.getbuffer(image))
            time.sleep(10)
            epd.init(epd.FULL_UPDATE)
            epd.Clear(0xFF)
        except Exception as e:
            print(e)
    else: #Action for no faces
        print('No faces detected')
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        draw.text((35, 45), 'No faces detected', font = font20, fill = 0)
        image = image.transpose(Image.ROTATE_180) #rotates image
        epd.display(epd.getbuffer(image))
        time.sleep(2)
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

    os.remove("img.jpg")
