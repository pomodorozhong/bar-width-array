import tensorflow.keras.preprocessing.image as image
from PIL import Image
import numpy as np
import barcode
import regex
import os

"""### Generating Barcode"""

import barcode
from barcode.writer import ImageWriter


# function that reads an image barcode.png as argument and process that image  to display the array
def barcodeworking():
    """### Croping image"""

    imag = Image.open('barcode.png').convert("L")
    w, h = imag.size
    # left,top,right,bottom
    region = imag.crop((0, 20, w, h-150))
    # region.save("regions.png")
    img = region
    """### Image Processing"""

    # img=image.load_img("regions.png",color_mode="grayscale")
    img = image.img_to_array(img)
    # CONVERTING TO FLOAT
    img = (img >= 200).astype("float")
    img = img.sum(axis=0)
    img = (img > 0).astype("float")
    img = np.squeeze(img)
    img = np.array(img, dtype=int)

    """### reading occurence of 0 and 1"""

    st = "".join(str(v) for v in img)
    all_matches = []
    # 0 for black strips
    for x in regex.finditer("0+", st):
        all_matches.append((0, x.start(), x.end()-x.start()))
    # 1 for white strips
    for x in regex.finditer("1+", st):
        all_matches.append((1, x.start(), x.end()-x.start()))
    # printing all matches
    # print(all_matches)

    # sorting them by index
    bars = sorted(all_matches, key=(lambda x: x[1]))
    bars = [(x[0], x[2]) for x in bars]

    # poping forst and last redundent values
    bars.pop(0)
    bars.pop()

    # taking minimum value as the factor for multiplication
    mn = min([x[1] for x in bars])
    # diving each value by min to get the space
    bars = [(x[0], int(x[1]/mn)) for x in bars]
    bars = [("white", x[1]) if x[0] == 1 else ("black", x[1]) for x in bars]
    print('\nLabeled array:')
    print('\n', bars)
    print('\nRaw Array\n')
    array = []
    for x in bars:
        array.append(x[1])
    print(array, '\n')

    os.remove('barcode.png')


while True:
    inp = input(
        'Select the number of your barcode choice\n1-EAN-8\n2-CODE 128\n3-CODE 39\n0-QUIT\n\n')
    # for ean 8 barcod type
    if inp == '1' or inp == 'EAN-8' or inp == 'ean-8' or inp == 'ean':
        print("EAN-8 is working and  requires minimum 7 numbers\n")
        code = input("Enter code of your barcode:\n")
        # running code thrugh the package
        EAN = barcode.get_barcode_class('ean8')
        ean = EAN(code)
        # storing svg for display
        ean.save('SVG_IMAGE')
        # using image writer for ong image to use in processing
        png = EAN(code, writer=ImageWriter())
        imag = png.save('barcode')
        barcodeworking()

    elif inp == '2' or inp == 'CODE 128' or inp == 'code 128' or inp == 'c128' or inp == 'C128':
        print("CODE 128 is working\n")
        code = input("Enter code of your barcode:\n")
        C128 = barcode.get_barcode_class('code128')
        c128 = C128(code)
        c128.save('SVG_IMAGE')
        png = C128(code, writer=ImageWriter())
        imag = png.save('barcode')
        barcodeworking()

    elif inp == '3' or inp == 'CODE 39' or inp == 'code 39' or inp == 'code39' or inp == 'c39' or inp == 'C39':
        print("CODE 39 is working\n")
        code = input("Enter code for barcode\n")
        C39 = barcode.get_barcode_class('code39')
        c39 = C39(code, add_checksum=False)  # checksum is false by default
        c39.save('SVG_IMAGE')
        png = C39(code, writer=ImageWriter(), add_checksum=False)
        imag = png.save('barcode')
        barcodeworking()
    elif inp == '0':
        break
    else:
        print("Select the correct number from options")
