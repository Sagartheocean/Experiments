import win32com.client       # Need pywin32 from pip
from PIL import ImageGrab    # Need PIL as well
import os

excel = win32com.client.Dispatch("Excel.Application")
workbook = excel.ActiveWorkbook

wb_folder = workbook.Path
wb_name = workbook.Name
wb_path = os.path.join(wb_folder, wb_name)

print "Extracting images from %s" % wb_path

image_no = 0

for sheet in workbook.Worksheets:
    for n, shape in enumerate(sheet.Shapes):
        if shape.Name.startswith("Picture"):
            # Some debug output for console
            image_no += 1
            print "---- Image No. %07i ----" % image_no

            # Sequence number the pictures, if there's more than one
            num = "" if n == 0 else "_%03i" % n

            filename = sheet.Name + num + ".png"
            file_path = os.path.join (wb_folder, filename)

            print "Saving as %s" % file_path    # Debug output

            shape.Copy() # Copies from Excel to Windows clipboard

            # Use PIL (python imaging library) to save from Windows clipboard
            # to a file
            image = ImageGrab.grabclipboard()
            try:
                filename = sheet.Name + num + ".jpeg"
                file_path = os.path.join(wb_folder, filename)
                image.save(file_path,'jpeg')
            except:
                try:
                    filename = sheet.Name + num + ".png"
                    file_path = os.path.join(wb_folder, filename)
                    image.save(file_path, 'png')
                except:
                    try:
                        filename = sheet.Name + num + ".bmp"
                        file_path = os.path.join(wb_folder, filename)
                        image.save(file_path, 'bmp')
                    except:
                        print("Could not download :" + str(filename))
