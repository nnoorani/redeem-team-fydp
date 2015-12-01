#!/usr/bin/python
from sys import argv
import zbar
from PIL import Image

def decode (theimage):  
    # create a reader
    scanner = zbar.ImageScanner()
    # configure the reader
    scanner.parse_config('enable')
    # obtain image data
    pil = Image.open(theimage).convert('L')
    width, height = pil.size
    raw = pil.tostring()
    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)
    # scan the image for barcodes
    barcode = 0 
    if scanner.scan(image):
        for symbol in image:
            barcode = int(symbol.data)
            return barcode               
            #what if there are 2 barcodes?                                                               
    else:
        return False

    del(image)

    


def decoded_array(array):
    for k in range (0, len(array)):
        array[k] = decode(array[k])
    return array 


def select_barcode(array):
    new_array = []
    for j in range (0, len(array)):
        if not array[j] == False:
            new_array.append(array[j])

    if len(new_array) == 0:
        print 'no array size'
        return False

    if len(new_array) ==1:
        return new_array[0]
    
    else:
        new_array.sort()
        print new_array
        for j in range(0,len(new_array)):
            for l in range(j+1,len(new_array)):
                if new_array[j] == new_array[l]:
                    return new_array[j]

# test code 
hey = ['pic (2).png', 'pic (2).png', 'pic (3).png', 'pic (2).png', 'pic (2).png', 'pic (6).png','pic (7).png','pic (7).png','pic (2).png']
new_array = decoded_array(hey)
code = select_barcode(new_array)
print code