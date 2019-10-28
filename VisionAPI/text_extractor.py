## Imports
from google.cloud import vision
from google.cloud.vision import types
import warnings
import io
from PIL import Image, ImageDraw
from enum import Enum
import argparse
#import cv2
import os
import glob
import pandas as pd
import re
import shutil
import time


client = vision.ImageAnnotatorClient()
warnings.filterwarnings("ignore")


## Extracts text from an image
def detect_text(path):
    """
    Detects texts in an image file.
    
    Arg(s)
    ------
    
    path: str
        file path for the image
    
    """

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)

    annotation = response.full_text_annotation
    
    breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType # a Vision method that identifies types of breaks in the text
    paragraphs = []
    lines = []

    for page in annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                para = ""
                line = ""
                for word in paragraph.words:
                    for symbol in word.symbols:
                        line += symbol.text
                        if symbol.property.detected_break.type == breaks.SPACE:
                            line += ' '
                        if symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
                            line += ' '
                            lines.append(line)
                            para += line
                            line = ''
                        if symbol.property.detected_break.type == breaks.LINE_BREAK:
                            lines.append(line)
                            para += line
                            line = ''
                            
                lines.append(line)
                paragraphs.append(para)

    return paragraphs
    #return lines

## [End of detect_text function]

## Iterate over folder of images to create a list of lists.
# Returns a list of pathnames that match pathname, which is a string containing a path specification.
path_list = glob.glob('./data/*.png') 


def image_loop(path_list):
    """
    Iterates through all the image files in the folder
    
    Arg(s):
    -------
    
    path_list: str
        list of file paths to all images in the folder
        
    """
    text_list = []
    for file in path_list:
        output = detect_text(file)
        text_list.append(output)
    
    return text_list

## [End of image_loop function]


path_list = glob.glob('./test/*png')

def detect_language(path_list, dest_pt, dest_es, dest_en):
    """
    Detects text language and then categorizes the images accordingly.
    
    Arg(s):
    -------
    
    path_list: str
        list of filepaths
        
    dest_i: str
        destination folder for images with text containing Portuguese (pt), Spanish (es), and English (en) respectively.
        
    """
    
    for file in path_list:

        with io.open(file, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        #source = f'{file}'
        source = {file}
#         dest_pt = dest_pt
#         dest_es = dest_es
#         dest_en = dest_en

        if not texts:
            continue

        elif str(texts[0].locale) == 'pt-PT': # Portugese
            

            try:
                shutil.move(source, dest_pt)
            except IndexError:
                continue


        elif str(texts[0].locale) == 'es': # Spanish
            
            try:
                shutil.move(source, dest_es)
            except IndexError:
                continue
                
        elif str(texts[0].locale) == 'en': # English
            
            try:
                shutil.move(source, dest_en)
            except IndexError:
                continue

        else:
            pass

## [End of detect_language function]

## Write the output to a text file
#with open("text.txt", "w") as file:
#    file.write(str(text_list))

    
## Read the file for evaluation    
#with open("text.txt", "r") as file:
#    data = eval(file.readline())
    

## Removes empty string characters ('') from the list
    
def strip_empty_strings(text_list):
    """
    Removes empty strings from the list,
    and creates a new list without those characters.
    """

    tier_2 = []
    for i in text_list:
        tier_1 = []
        for j in i:
            if j != '':
                a = j 
                tier_1.append(a)
        tier_2.append(tier_1)
        
    return tier_2  

## [End of strip_empty_strings function]

## Creates a dataframe with three columns

def first_two_cols(text):
    """
    Returns a dataframe with two columns:
    1. Product Description
    2. Tag line
    
    """
    
    content = []
    for i in text:
        product_details = {}
        product_details['product_descr'] = i[0]
        product_details['tag_line'] = i[1]
        
        content.append(product_details)

    return pd.DataFrame(content)

## [End of first_three_cols function]



def tag_image(path_list, f_name='f_name'):
    """
    Creates a list of all image filenames
    """
    
    file_list = []
    for file in path_list:
        file_name = file.split(f_name)[1]
        file_list.append(file_name)

    return file_list

## [End of tag_image function]



def extract_insight(text):
    """
    Extracts text identified as the 'insight' column.
    Returns a list of lists containing this info for each image.
    """

    outer_list = []
    for i in text:
        inner_lists = []
        
        if i[3][0] != i[3][0].lower():
            insight = i[2] 
            inner_lists.append(insight)

        elif i[4][0] == i[4][0].lower():
            insight = i[2] + i[3] + i[4]
            inner_lists.append(insight)

        else:
            insight = i[2] + i[3]
            inner_lists.append(insight)

        outer_list.append(inner_lists)
        
    return outer_list




#insight_list = extract_insight(text_lines)

## [End of extract_insight]



def insight_col(text):
    """
    Returns a dataframe with the insight column.
    
    """
    
    content = []
    for i in text:
        for j in i:
            product_details = {}
            product_details['insight'] = j
            content.append(product_details)

    return pd.DataFrame(content)

## [End of insight_col function]

def price_table(text_file):
    price_list = []
    for index_1, i in enumerate(text_file):
        for index_2, j in enumerate(i):
            prices = {}
            if (j.find(' $') != -1) or (j.find('$ ') != -1):
                prices['image_index'] = index_1
                prices['price'] = j
                print index_1
                print j
            else:
                continue
            price_list.append(prices)
    return price_list
    #return pd.DataFrame(price_list)


def extract_size(text_file):
    df = pd.DataFrame(columns=['index', 'variant', 'size','price'])
    overall_list=[]
    file_index = 0
    for list_of_str in text_file:
        file_list = []
        #print ("file:"+str(file_index))
        for str in list_of_str:
            x = re.findall(r"\dg|\dml|\dL", str)
            i = 0
            if (x):
                words = str.split()
                while i < len(words):
                    variant =""
                    price = ""
                    size = ""
                    x = re.findall(r"\dg|\dml|\dL", words[i])
                    # print(x)
                    if (x):
                        if i > 0:  # for finding the variant
                            print ("Variant: " + words[i - 1])
                            variant = words[i - 1]
                        print("Size:" + words[i])
                        size = words[i]

                        if ("$" in str and len(words) > i + 1):
                            if ("$" in words[i + 1]):
                                print ("price:" + words[i + 1])
                                price =words[i + 1]

                    #else:
                    #    print("--")

                    #adding elements to the list
                    file_list.append([file_index, variant, size, price ])
                    i += 1

        #write for image 1
        if len(file_list)>0:
            overall_list.append(file_list)
        else:
            overall_list.append([file_index])
        file_index+=1
    return overall_list

##--- End of functions
path_list = glob.glob('C:\Users\Sagar Raythatha\Desktop\CIC\images\New folder\*png')
text_lines = image_loop(path_list)
text_lines = strip_empty_strings(text_lines)
print text_lines
df = pd.DataFrame()
df = first_two_cols(text_lines)
insight_list = extract_insight(text_lines)
df['insight'] = insight_col(insight_list)
price_df  =pd.DataFrame()
#print price_table(text_lines)
list = extract_size(text_lines)
print list