database = {
	"6820020094" : "products/chocolate-milk.jpg",
	"06741806" : "products/fanta.jpg"
}


def select_barcodes(barcodes): 
	barcodes_to_lookup = []
	for j in range(0,len(barcodes)):
	    for l in range(j+1,len(barcodes)):
	        if barcodes[j] == barcodes[l]:
	           barcodes_to_lookup.append(barcodes[j])
	return barcodes_to_lookup

def product_lookup(barcodes):
	for i in barcodes:
		if database[i]:
			image = Image.open(database[i])
			image.show()	