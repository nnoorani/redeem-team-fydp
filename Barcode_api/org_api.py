import requests
import simplejson as json
import urllib 
import mechanize 
from bs4 import BeautifulSoup


def database_search(barcode):
	url = 'http://api.upcdatabase.org/json/c25726d8a3ece25702c725d92e331b33/'
	
 	# barcode = '73728232059'	
	# barcode ='058500000242'
	# barcode = '051500686485'


	final = url+barcode
	try:
		r = requests.get(final).json()
		print r['itemname']
		return r['itemname']
	except:
		print ("could not retrieve from database")



def getPic (search):
    search = search.replace(" ","%20")
    try:
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.addheaders = [('User-agent','Mozilla')]
        # htmltext = browser.open("https://www.google.com/search?site=imghp&tbm=isch&source=hp&biw=1414&bih=709&q="+search+"&oq="+search)
        htmltext = browser.open("https://www.google.nl/search?tbm=isch&q="+search)
        img_urls = []
        
        formatted_images = []
        soup = BeautifulSoup(htmltext)
        # print soup
        results = soup.findAll("img")

        # for r in results:
            # print r
        
        image = results[0]['src']

        return  image

    except:
        return []

def savePic(url):
    urllib.urlretrieve(url,'image.jpg')
    
# itemname = database_search('73728232059')
link = getPic('girl')   
savePic(link)



