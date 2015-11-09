import os
import glob
import shutil
from PIL import Image

sets = [
    'bottle',
    'bottle_colored',
    'chips',
    'granola',
    'peanut'
]

sides = ['left', 'left', 'left', 'right', 'right', 'right', 'left', 'left', 'left',  'right', 'right', 'right']

orientations = [
'portrait',
'landscape'
]

angles = [
'60', '45', '30', '30', '45', '60', '60', '45', '30', '30', '45', '60'
]

curr_dir = os.getcwd()
files = os.listdir(curr_dir)
del files[0]

print(len(files), files)
side = 1

for f in files:
	index = files.index(f)
	path = 'granola_'

	if index > 5:
		path+= sides[index] + '_' + angles[index] + '_' + orientations[0] + '.jpg'
	else:
		path+= sides[index] + '_' + angles[index] + '_' + orientations[1] + '.jpg'

	print(path)
	os.rename(f, path)



