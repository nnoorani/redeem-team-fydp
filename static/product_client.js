ws = new WebSocket("ws://localhost:5000/");
var productList = $("div.product-list"),
productImage = $(".product-image > img"),
productImageContainer = $(".product-image-container"),
cueBox = $(".cue-box"),
objectEntered;
  // Set event handlers.
ws.onopen = function() {
    console.log("onopen");
};
  
ws.onmessage = function(json) {
    // e.data contains received string.
    var data = JSON.parse(json.data);
    console.log(data);
    	// this is if it's actual product info
	if (data.name) {
		barcodeFound = true;
		// if it has a name, assume its a product
		display_just_scanned(product);
		display_product_info(product);
	} else if (data.objectEntered) {
		objectEntered = true;
		barcodeFound = false;
		displayWait();
	} else if (data.objectLeft) {
		if (objectEntered && !barcodeFound) {
			handle_missed_detection();
		}
		objectEntered = false;
		displayCue();
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

	return product_html_string
};

function addToTotal(amount) {
	var total = $(".total-sum"),
	intTotal = parseInt(total.html().split('$')[1]),
	intAmount = parseInt(amount), 
	newTotal = intTotal + intAmount;

	total.html("$" + newTotal.toString());
}

function handle_missed_detection() {
	cueBox.html("Oops! The last item was not scanned. Please re-enter the item into the scanner");
}

function displayCue() {
	if (cueBox.hasClass('wait')) {
		// check if we missed the last detection
		cueBox.addClass('go');
		cueBox.html("Place next item behind the black line")
	} else {
		cueBox.addClass('go');
		cueBox.html("Place next item behind the black line")	
	}
}

function displayWait() {
	if (cueBox.hasClass('go')) {
		cueBox.addClass('wait');
		cueBox.html("Please wait to place your item")
		cueBox.removeClass('go');
	} else {
		cueBox.addClass('wait');
		cueBox.html("Please wait to place your item");
	}
}

// setInterval(function(){
// 	if (cueBox.hasClass('wait')) {
// 		// check if we missed the last detection
// 			cueBox.addClass('go');
// 			cueBox.html("Place next item behind the black line")
// 			setTimeout(function(){
// 				if (cueBox.hasClass('go')) {
// 					cueBox.addClass('wait');
// 					cueBox.html("Please wait to place your item")
// 					cueBox.removeClass('go');
// 				}
// 			}, 3000);
// 			cueBox.removeClass('wait');
// 		} 
// 		// else if (!barcodeFound) {
// 		// 	cueBox.addClass('missed');
// 		// 	cueBox.html("The last item was not found, please scan it again");
// 		// }
// }, 6000);
