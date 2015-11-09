import os 

speeds = ['2', '20', '100', '200', '400', '800'] #actual shutter speed is 1/number
curr_dir = os.getcwd()
files = os.listdir(curr_dir)

for f in files:
	index = files.index(f)
	item = str(os.path.relpath(curr_dir,".."))


	path = item + '_1_' + speeds[index] + '.jpg'
	print path
	os.rename(f, path)