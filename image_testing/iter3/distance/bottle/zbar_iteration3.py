#!/usr/bin/python
from sys import argv
import zbar
from PIL import Image

def process (theimage):	
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

    if scanner.scan(image):
    # extract results
        for symbol in image:
        # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
    else:
        print 'did not decode'

    # clean up
    del(image)

distance = [
    '10',
    '25',
    '37.5',
    '50',
    '60'
]

sets = [
    'bottle',
    'bottle_colored',
    'chips',
    'granola',
    'peanut'
]

#distances/resolution
for j in range(0,len(sets)):
    for i in range(0,len(distance)):
        path = sets[j] + "_" + distance[i] +"cm_0degree.jpg"
        print path
        process(path)
