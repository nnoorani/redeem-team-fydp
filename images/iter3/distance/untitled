import os
import shutil
from PIL import Image


sets = [
    # 'bottle',
    # 'bottle_colored',
    'chips',
    'granola',
    'peanut'
]

distance = [
    '10',
    '25',
    '37.5',
    '50',
    '60'
]

resolution = [
'1280',
'1024',
'800',
'640',
'320'
]

test_img = Image.open('chips_10cm_0degree.jpg')
max_width, max_height = test_img.size
print (max_height)
print (max_width)

for i in sets: 
	for j in distance:
		for k in resolution: 

			dst = i + '_' + j + 'cm_0degree_' + k + '.jpg'
			src = i + '_' + j + 'cm_0degree.jpg'
			width_ratio = float(k) / max_width
			new_height = max_height * width_ratio
			new_size = (k, new_height)
			img = Image.new('RGB',(max_width, max_height), 444)
			img.save(dst, "JPEG")
			del(img)
			shutil.copy(src, dst)

			new_img = Image.open(dst)
			print(int(k), int(new_height))
			new_img = new_img.resize((int(k), int(new_height)), Image.ANTIALIAS)
			width, height = new_img.size
			new_img.save(dst, "JPEG")
			print (width)
			print (height)
			


