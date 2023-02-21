import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import os

def makescript(imagepaths,textdir,textname):
    try:
        os.mkdir(textdir)
    except FileExistsError:
        pass
    text =""
    for imagepath in imagepaths:
        with Image.open(imagepath) as image:
            text +=f"{imagepath};"
            text += tess.image_to_string(image).replace("\n",".").replace(";"," ")+"\n"


    textfile = open(f"{textdir}\\{textname}","w")
    textfile.write(text)
    textfile.close()