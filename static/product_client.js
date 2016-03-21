ws = new WebSocket("ws://localhost:5000/");
var productList = $("div.product-list"),
productImage = $(".product-image > img"),
cueBox = $(".cue-box"),
objectEntered = True;
  // Set event handlers.
ws.onopen = function() {
    console.log("onopen");
};
  
ws.onmessage = function(product_json) {
    // e.data contains received string.
    var product = JSON.parse(product_json.data);
    console.log(product);

    if (product.name) {
    	// this is if it's actual product info
    	display_just_scanned(product);
    	display_product_info(product);
    	if (objectEntered) {
    		barcodeFound = True
    	}
    }

    if (product.objectEntered) {
    	objectEntered = True;
    	barcodeFound = False
    }
};
  
ws.onclose = function() {
    console.log("onclose");
};
ws.onerror = function(e) {
	console.log("onerror");
	console.log(e)
};

function display_just_scanned(product) {
	var urlForImage;
	urlForImage = "../static/" + product["img-url"];
	productImage.attr("src", urlForImage)
}

function display_product_info(product) {
	product_html = construct_product_html(product);
	if (product.price) {
		addToTotal(product.price);
	}
	productList.append(product_html);
};

function construct_product_html(product) {
	product_html_string = '<div class="product-row col-md-12">' +
	    '<div class="product-name col-md-10">'+product.name+'</div>' + 
	    '<div class="product-price col-md-2">'+product.price+'</div></div>';
};

function addToTotal(amount) {
	var total = $(".total-sum"),
	intTotal = parseInt(total.html().split('$')[1]),
	intAmount = parseInt(amount), 
	newTotal = intTotal + intAmount;

	total.html("$" + newTotal.toString());
}

function handle_missed_detection() {

}

setInterval(function(){
	if (cueBox.hasClass('wait')) {
		// check if we missed the last detection
		if barcodeFound {
			cueBox.addClass('go');
			cueBox.html("Place next item behind the black line")
			setTimeout(function(){
				if (cueBox.hasClass('go')) {
					cueBox.addClass('wait');
					cueBox.html("Please wait to place your item")
					cueBox.removeClass('go');
				}
			}, 3000);
			cueBox.removeClass('wait');
		} else if (!barcodeFound) {
			cueBox.addClass('missed');
			cueBox.html("The last item was not found, please scan it again");
		}
	}
}, 6000);
