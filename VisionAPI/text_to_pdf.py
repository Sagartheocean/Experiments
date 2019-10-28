import fpdf
import os



def text_to_pdf():

    path = "C:\Users\Sagar Raythatha\Desktop\CIC\images\\texts"
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            filename = os.path.join(path, f)
            file1 = open(filename, "r")
            content = file1.read()
            file1.close()

            pdf = fpdf.FPDF(format='letter')
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            #pdf.cell(40,10,txt=content)
            pdf.write(5, content, 'http://www.fpdf.org')
            pdf.output(str(filename) + ".pdf")

text_to_pdf()