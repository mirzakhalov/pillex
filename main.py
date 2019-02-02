from enhancer import Enhancer
from vision import Vision
import urllib.request
import json
import sys
from detect_shapes import ShapeDetection


imagepath = "result.jpg"


def main():
    # increase the contrast of the image to make the labels more visible
    enhancer = Enhancer()
    enhancer.enhance(imagepath)
    # get the labels from the Google Vision OCR
    vision = Vision()
    labels = vision.detect_document(imagepath)
    print(labels)

    ShapeDetection.detect(imagepath)
    # use Google Vision to detect dominant colors, then extract common color name using a custom library
    colors = vision.detect_properties(imagepath)
    print(colors)
    if len(labels) == 0 or len(colors) == 0:
        print('Could not classify')
        quit()
    # create the api call string, concatinating all the results
    api_call = "https://rximage.nlm.nih.gov/api/rximage/1/rxnav?color=" + colors[0]
    # concatinate more if there are more than 1 imprints
    for i in range(0, len(labels)):
        api_call = api_call + "&imprint=" + labels[i]
    print(api_call)
    # make the API GET request
    contents = urllib.request.urlopen(api_call).read()
    # converts the bytes object to string, then to json
    json_response = json.loads(contents.decode())
    # get the number of matches
    matches_count = int(json_response['replyStatus']['imageCount'])
    for i in range(0, matches_count):
        name = json_response['nlmRxImages'][i]['name']
        print(name)



if __name__ == "__main__":
    main()