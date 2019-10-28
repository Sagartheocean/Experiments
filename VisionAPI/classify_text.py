import extract_text
import os
import csv

def map_line_with_csv(line_text):
    #read csv
    reader = csv.reader(open("C:\ProjectRepos\Experiments\VisionAPI\product_title.csv"))
    flag = False
    for row in reader:
        if row[0] == line_text:
            print ("matching : "+ line_text)
            flag = True
    if not flag:
        print (line_text + " is not matching")



    #for line_text in reader.next():
    #    print("key : " + line_text + " is present")


def get_product_details(path):
    product_details = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            filename = os.path.join(path, f)
            texts = extract_text.detect_text(filename)
            y_list = extract_text.get_y_for_words(texts)
            lines = extract_text.get_text_lines(y_list, texts)
            product_title = lines[0]
            tag_line = lines[1]
            print ("Product Title:" + product_title)
            print ("Tag line:" + tag_line)
            detail = [f, product_title, tag_line]
            product_details.append(detail)
    return product_details


def write_extracted_text(path):
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            filename = os.path.join(path, f)
            texts = extract_text.detect_text(filename)
            f = open(path + "\\texts\\" + f + ".txt", "w+")
            try:
                f.write(texts[0].description)
            except:
                print (str(f) + " is not converted into text")
            f.close()

if __name__ == '__main__':
    path = "C:\Users\Sagar Raythatha\Desktop\CIC\images"
    credentials = extract_text.get_credentials()
    #product_titles = get_product_details(path)
    #print (product_titles)

    write_extracted_text(path)
