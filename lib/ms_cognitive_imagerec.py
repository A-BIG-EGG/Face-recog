import http.client, urllib, base64, json
import requests
from collections import namedtuple
import operator

# change this
#   the subscription and endpoints for Face API and Vision API
#   make sure endpoint is correct for your region, default is western us
face_api_sub_key = 'a760241aebe44b1c80eab0e5e42425c7'
face_api_endpoint = 'https://uksouthface.cognitiveservices.azure.com/face/v1.0/detect'

vision_api_sub_key = 'cfad2127edc14f7f87466cf03731044b'
vision_api_endpoint = 'https://uksouthvision.cognitiveservices.azure.com/'


class FaceAttribs(object):
    """__init__() functions as the class constructor"""
    def __init__(self, age=None, gender=None, gender_noun=None, gender_possessive=None, glasses=None, glasses_txt=None, top_emotion=None, top_emotion_conf=None, profile_txt=None):
        self.age = age
        self.gender = gender
        self.gender_noun = gender_noun
        self.gender_possessive = gender_possessive
        self.glasses = glasses
        self.top_emotion = top_emotion
        self.top_emotion_conf = top_emotion_conf
        self.profile_txt = profile_txt
        self.glasses_txt = glasses_txt


def ms_GetFaceAttribs (face):

    if len(face)> 0:

        faceAttribs = FaceAttribs()
        print(face["faceAttributes"]["age"])

        faceAttribs.age = face["faceAttributes"]["age"]
        faceAttribs.gender = face["faceAttributes"]["gender"]
        faceAttribs.glasses = face["faceAttributes"]["glasses"]
        faceAttribs.bald_conf = face["faceAttributes"]["hair"]["bald"]*100

        if faceAttribs.gender == 'male' :
            faceAttribs.gender_noun = "he"
            faceAttribs.gender_noun_s = "he's"
            faceAttribs.gender_possessive = "his"
            faceAttribs.gender_noun_cap = "He"
            faceAttribs.gender_possessive_cap = "His"
        else:
            faceAttribs.gender_noun= "she"
            faceAttribs.gender_noun_s = "she's"
            faceAttribs.gender_possessive = "her"
            faceAttribs.gender_noun_cap = "She"
            faceAttribs.gender_possessive_cap = "Her"

        emotion = face["faceAttributes"]["emotion"]
        haircolor = face["faceAttributes"]["hair"]["hairColor"]

        sort_emotion = sorted(emotion.items(), key=operator.itemgetter(1), reverse=True)
        sort_haircolor = sorted(haircolor, key=lambda d: d["confidence"], reverse=True)

        if faceAttribs.glasses == 'NoGlasses':
            faceAttribs.glasses_txt = "No Glasses"
        else:
            faceAttribs.glasses_txt = "wearing %s"% (faceAttribs.glasses)

        print(sort_haircolor[0])
        print(sort_emotion)
        faceAttribs.top_emotion = sort_emotion[0][0]
        faceAttribs.top_emotion_conf = sort_emotion[0][1] *100
        faceAttribs.top_haircolor = sort_haircolor[0][0][1]
        faceAttribs.top_haircolor_conf = sort_haircolor[0][1][1] *100
        faceAttribs.profile_txt = "%s age %d"% (faceAttribs.gender, faceAttribs.age)


        return faceAttribs
    else:
        return False

def ms_WhoDoYouSee (body):

    # Request headers.
    header = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': face_api_sub_key
    }

    # Request parameters.
    params = {
        'returnFaceId': 'true',
       # 'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile,emotion,glasses,hair',
    }

    try:

        api_url = face_api_endpoint

        response = requests.post(api_url, data=body, headers=header, params=params)

        #print (response.json())
        #response = conn.request('POST', uri_base + '/face/v1.0/detect', json=body, data=body, headers=headers, params=params)
        #data = response.read().decode('utf-8')

        print ('Response:')
        parsed = json.loads(response.text)
        print (json.dumps(parsed, sort_keys=True, indent=2))

        #faceID = parsed[0]["faceId"]
       # print("faceID = %s"% faceID)

        #height = parsed[0]["faceRectangle"]["height"]
        #print("height= %d"% height)

        #gender = parsed[0]["gender"]
        #print("gender = %s"% gender)


    except Exception as e:
        print('Error:')
        print(e)

    return(parsed)


def ms_WhatDoYouSee (body):

    headers = {
        # Request headers.
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': vision_api_sub_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters. All of them are optional.
        'visualFeatures': 'Description, Faces',
        'details': '',
        'language': 'en',
    })

        # Execute the REST API call and get the response.

    try:
        conn = http.client.HTTPSConnection(vision_api_endpoint)
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        parsedText = "I see %s"% (parsed['description']['captions'][0]['text'])
        conn.close()

    except Exception as e:
        print('Error:')
        print(e) ########### Python 3.6 #############
        parsedText = e

    return parsedText
