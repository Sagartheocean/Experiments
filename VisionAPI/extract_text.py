from google.cloud import vision
from google.cloud.vision import types
import io
import os
from oauth2client.client import GoogleCredentials
from enum import Enum
from PIL import Image, ImageDraw
import shutil
import datetime
import time
# Parallelizing using Pool.map()
import multiprocessing as mp


SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
          'https://www.googleapis.com/auth/cloud-vision']

mypath = "C:\Users\Sagar Raythatha\Desktop\CIC\New folder\Colgate HC 2011-2014_1_files"

GOOG_CRED = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

imageName = "product1.png"

def get_credentials():
    """Get the Google credentials needed to access our services."""
    credentials = GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
            credentials = credentials.create_scoped(SCOPES)
    return credentials


def detect_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    print (texts[0].description)
    #del texts[0]
#    print (y_list)
    #get_text_lines(y_list, texts)
    return texts


def get_y_for_words(texts):
    y_list = []

    for text in texts:
        #print('\n"{}"'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])
        y_list.append(text.bounding_poly.vertices[1].y)
        # y_list.append(text.description)
        #print("font size" + str(text.bounding_poly.vertices[1].y - text.bounding_poly.vertices[2].y))
        #print('bounds: {}'.format(','.join(vertices)))

    return y_list


def get_text_lines(y_list, texts):

    list_indexes = get_line_separator(y_list, texts)
    lines = []
    line = ""
    for sublist_indexes in list_indexes:
        for indexes in sublist_indexes:
            line = line + " " + str(texts[indexes].description).encode('utf-8')
        lines.append(line)
        line = ""
    print lines
    return lines
    get_avg_font_size(list_indexes, texts)


def get_line_separator(y_list, texts):
    list_indexes = []
    sublist_indexes = [0]
    index = 0
    while(len(y_list)-1>index):
        if(y_list[index+1] == y_list[index]):
            sublist_indexes.append(index+1)
        else:
            if(check_minor_diff(texts, index)):
                sublist_indexes.append(index+1)
            else:
                list_indexes.append(sublist_indexes)
                sublist_indexes=[]
                sublist_indexes.append(index+1)
        index = index+1
    print(list_indexes)
    return list_indexes


def check_minor_diff(texts, index):
    #it will check the whether the next element can be added into the same line
    word_size = abs(texts[index].bounding_poly.vertices[1].y - texts[index].bounding_poly.vertices[2].y)
    elem_diff_y = abs(texts[index].bounding_poly.vertices[1].y - texts[index+1].bounding_poly.vertices[1].y)
    elem_diff_y2 = abs(texts[index].bounding_poly.vertices[2].y - texts[index + 1].bounding_poly.vertices[2].y)
    if(elem_diff_y==0 or elem_diff_y2 == 0):
        return True
    else:
        if word_size/elem_diff_y >= 2 or word_size/elem_diff_y2 >= 2:
            return True
        elif (texts[index].bounding_poly.vertices[1].y > texts[index+1].bounding_poly.vertices[1].y) and (texts[index].bounding_poly.vertices[2].y < texts[index+1].bounding_poly.vertices[2].y):
            return True
        elif (texts[index].bounding_poly.vertices[1].y < texts[index + 1].bounding_poly.vertices[1].y) and (
                texts[index].bounding_poly.vertices[2].y > texts[index + 1].bounding_poly.vertices[2].y):
            return True
        else:
            return False


def get_avg_font_size(list_indexes, texts):
    font_size = []
    for sublist_indexes in list_indexes:
        diff = 0
        for index in sublist_indexes:
            diff = diff + abs(texts[index].bounding_poly.vertices[1].y - texts[index].bounding_poly.vertices[2].y)
        avg_diff = diff/len(sublist_indexes)
        font_size.append(avg_diff)
    print font_size
    return font_size


def getLabels():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath('product1.png')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)




def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def get_document_bounds(image_file, feature):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def detect_language(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    #print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    #print ("language:" + str(texts[0].locale))
    splittedList = path.split("\\")
    filename = splittedList[len(splittedList) - 1]
    filepath = "\\".join(splittedList[0:len(splittedList) - 1])

    if str(texts[0].locale) == "es":
        # copy images to es folder
        dst = filepath + "\\" + "es" + "\\" + filename
        dst = filepath + "\\" + "es"
        shutil.move(path, dst)

    elif str(texts[0].locale) == "en":
        # copy images to en folder
        dst = filepath + "\\" + "en" + "\\" + filename
        dst = filepath + "\\" + "en"
        shutil.move(path, dst)

    elif str(texts[0].locale) == "pt-PT":
        # copy images to en folder
        dst = filepath + "\\" + "pt-PT" + "\\" + filename
        dst = filepath + "\\" + "pt-PT"
        shutil.move(path, dst)


def detect_language_parallel(f):
    if os.path.isfile(os.path.join(mypath, f)):
        filename = os.path.join(mypath, f)
        try:
            detect_language(filename)
        except:
            print ("error in file: " + str(filename))



if __name__ == '__main__':

    credentials = get_credentials()

    #image size
    im = Image.open('C:\Users\Sagar Raythatha\Desktop\CIC\New folder\Colgate HC 2011-2014_1_files\en\image016.png')
    width, height = im.size
    print(str(width) + "*" + str(height))

    #for detecting language and put it in a seperate folder
    #pool = mp.Pool(mp.cpu_count())
    #results = pool.map(detect_language_parallel, [f for f in os.listdir(mypath)])
    #pool.close()

    #detectting text, lines & font size
    #detect_text("C:\Users\Sagar Raythatha\Desktop\CIC\New folder\Colgate HC 2011-2014_1_files\en\image016.png")


    # getting labels out of the text
    #getLabels()


    #for getting bounds of paragraph and drawing it
    #image = Image.open(imageName)
    bounds = detect_text("C:\Users\Sagar Raythatha\Desktop\CIC\images\image100.png")
    #bounds = get_document_bounds("C:\Users\Sagar Raythatha\Desktop\CIC\images\image100.png", FeatureType.PARA)
    #print(bounds)
    #draw_boxes(image, bounds, 'red')
    #image.save("image with blockbox.png")
