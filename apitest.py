import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from lib.ms_cognitive_imagerec import ms_WhatDoYouSee, ms_WhoDoYouSee, ms_GetFaceAttribs, FaceAttribs
from PIL import Image

body = Image.open('testsmile.JPG')
ttyt = ms_WhoDoYouSee(body)
#faceAttribs = ms_GetFaceAttribs(face)
print(str(ttyt))
