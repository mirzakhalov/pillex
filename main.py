from enhancer import Enhancer
from vision import Vision
import urllib.request
import json
import sys
from detect_shapes import ShapeDetection
from PIL import Image, ImageEnhance
import cv2


import pyrebase

# configuration keys for firebase
config = {
  "apiKey": "AIzaSyBHCM_96N-9mSl2NJyoxH_QzNayIrc3ZvE",
  "authDomain": "pillex.firebaseapp.com",
  "databaseURL": "https://pillex.firebaseio.com",
  "storageBucket": "pillex.appspot.com",
}

firebase = pyrebase.initialize_app(config)



# if the query fails with only imprint results, then try it in combination with colors
def try_with_colors(api_call, colors):
    for color in colors:
        contents = urllib.request.urlopen(api_call + "&color=" + color).read()
        # converts the bytes object to string, then to json
        json_response = json.loads(contents.decode())
        if len(json_response) > 0:
            return json_response
        time.sleep(1)
    
    return None

# grab the image from the database and rewrite it every time
def download_from_firebase(url):
    firebase.storage().child(url).download("downloaded.jpg")
    label = run("downloaded.jpg")
    return label

### enhane the image, get the labels and dominant colors. Then create an API call and analyze the results
def run(imagepath):
    # 
    enhancer = Enhancer()
    enhancer.enhance(imagepath)
   
    ##image = Image.open('pill3.jpg')
    ##image = ImageEnhance.Contrast(image).enhance(5)
    ##image.PIL.save("pic.jpg")
    
    ##quit()
    # get the labels from the Google Vision OCR
    vision = Vision()
    labels = vision.detect_document(imagepath)
    print(labels)
    # use Google Vision to detect dominant colors, then extract common color name using a custom library
    colors = vision.detect_properties(imagepath)
    print(colors)
    if len(labels) == 0 or len(colors) == 0:
        print('Could not classify')
        return 'Unidentified'
    
    api_call = "https://datadiscovery.nlm.nih.gov/resource/crzr-uvwg.json?" + "&splimprint=" + labels[0]
    # concatinate more if there are more than 1 imprints
    for i in range(1, len(labels)):
        api_call = api_call + ";" + labels[i]
    print(api_call)
    # make the API GET request
    contents = urllib.request.urlopen(api_call).read()
    # converts the bytes object to string, then to json
    json_response = json.loads(contents.decode())
    # get the number of matches
    if len(json_response) >= 1:
        return json_response[0]['medicine_name']
    elif len(json_response) < -1:
        json_res = try_with_colors(api_call, colors)
        if json_res == None:
            return 'Unidentified'
        else:
            return json_res[0]['medicine_name']
    else:
        return 'Unidentified'

def stream_handler(message):
    print(message)
    if message["event"] == "put":
        imageID = message['path']
        imageID = imageID[1:]
        if imageID != "":
            label = download_from_firebase(message['data'])
            firebase.database().child("users/jim/outputs/"+ imageID).set(label)
            print(label)
            print(message['data'])
    else:
        print(message["event"])

#run("result.jpg")
my_stream = firebase.database().child("users/jim/images").stream(stream_handler)
import time
while True:
    print("Waiting...")
    time.sleep(5)

quit()

