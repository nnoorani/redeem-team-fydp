import os
import shutil
from PIL import Image

sets = [
    'bottle',
    'bottle_colored',
    'chips',
    'granola',
    'peanut'
]

sides = [
'left',
'right'
]

orientations = [
'portrait',
'landscape'
]

angles = [
'60', '45', '30', '30', '45', '60'
]

curr_dir = os.getcwd()
files = os.listdir(curr_dir)

for f in files:
	index = files.index(f)
	landscape = 1
	if index > 5:
		index = index - 6
		landscape = 0
	path = 'bottle_'
	if index < 3:
		path += sides[0] + '_' + angles[index] + '_' 
	else:
		path += sides[1] + '_' + angles[index] + '_' 

	if landscape:
		path += orientations[1] + '.jpg'
	else: 
		path += orientations[0]	+ '.jpg'

	os.rename(f, path)



