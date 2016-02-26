import requests
import simplejson as json


def database_search(barcode):
	url = 'http://api.upcdatabase.org/json/c25726d8a3ece25702c725d92e331b33/'
	
 	# barcode = '73728232059'	
	# barcode ='058500000242'
	# barcode = '051500686485'


	final = url+barcode
	r = requests.get(final).json()
	print r['itemname']



database_search('73728232059')