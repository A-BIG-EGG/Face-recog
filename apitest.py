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

body = camera.get_frame()

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'a760241aebe44b1c80eab0e5e42425c7',
}

params = {
    'returnFaceId': 'true',
   # 'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,smile,emotion,glasses',
}

FaceApiDetect = 'https://uksouthface.cognitiveservices.azure.com/face/v1.0/detect'

try:
    # REST Call
    response = requests.post(FaceApiDetect, data=body, headers=headers, params=params)
    print("RESPONSE:" + str(response.json()))

except Exception as e:
    print(e)
