import io
import os
import webcolors

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


class Vision():

    def __init__(self):
        print("vision started...")
        self.output = []
        self.colors = []
        
    def detect_document(self,path):
        """Detects document features in an image."""
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.document_text_detection(image=image)

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                #print('\nBlock confidence: {}\n'.format(block.confidence))

                for paragraph in block.paragraphs:
                    #print('Paragraph confidence: {}'.format(
                    #    paragraph.confidence))

                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        #print('Word text: {} (confidence: {})'.format(
                        #    word_text, word.confidence))
                        self.output.append(word_text)
        
        return self.output

    def closest_colour(self,requested_colour):
        min_colours = {}
        for key, name in webcolors.html4_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_basic_colors(self, color):
        if color == 'silver' or color == 'grey':
            return 'gray'
        elif color == 'maroon':
            return 'red'
        elif color == 'fuchsia':
            return 'purple'
        elif color == 'lime':
            return 'green'
        elif color == 'olive':
            return 'yellow'
        elif color == 'navy' or color == 'aqua':
            return 'blue'
        elif color == 'teal':
            return 'blue'
        else:
            return color
        

    def detect_properties(self, path):
        """Detects image properties in the file."""
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.image_properties(image=image)
        props = response.image_properties_annotation
        #print('Properties:')

        for color in props.dominant_colors.colors:
            #print('fraction: {}'.format(color.pixel_fraction))
            #print('\tr: {}'.format(color.color.red))
            #print('\tg: {}'.format(color.color.green))
            #print('\tb: {}'.format(color.color.blue))
            #print('\ta: {}'.format(color.color.alpha))
            try:
                closest_name = actual_name = webcolors.rgb_to_name((int(color.color.red), int(color.color.green), int(color.color.blue)), spec =u'html4')
                actual_name = self.get_basic_colors(actual_name)
                self.colors.append(actual_name)
            except ValueError:
                closest_name = self.closest_colour((int(color.color.red), int(color.color.green), int(color.color.blue)))
                closest_name = self.get_basic_colors(closest_name)
                self.colors.append(closest_name)
        return self.colors
    