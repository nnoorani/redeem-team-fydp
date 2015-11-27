import os

for i in os.listdir(os.getcwd()):
	print i
	command = "zbarimg -q " + i
	os.system(command)


	