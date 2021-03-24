import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from lib.ms_cognitive_imagerec import ms_WhatDoYouSee, ms_WhoDoYouSee, ms_GetFaceAttribs, FaceAttribs
from PIL import Image
import requests

from camera_pi import Camera
camera = Camera()
image_file = 'image_file.png'
body = camera.get_frame()

#body = dict()
#body["url"] = "https://ichef.bbci.co.uk/images/ic/1024x576/p081lz7v.jpg"
#body = str(body)

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'a760241aebe44b1c80eab0e5e42425c7',
}

params = {
    'returnFaceId': 'true',
   # 'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,smile,emotion,glasses,hair',
}

FaceApiDetect = 'https://uksouthface.cognitiveservices.azure.com/face/v1.0/detect'

try:
    # REST Call
    #response = requests.post(FaceApiDetect, data=body, headers=headers, params=params)
    response = ms_WhoDoYouSee(body)
    print("RESPONSE:" + str(response.json()))

except Exception as e:
    print(e)
