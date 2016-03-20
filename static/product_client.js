var socket = io.connect('http://' + document.domain + ':' + location.port + '/test'),
productList = $("div.product-list"),
productImage = $(".product-image > img");

socket.on('connect', function() {
	socket.emit('request', "connected");
	setInterval(function() {
		socket.emit('checking');
	}, 100);
    socket.on('disconnect', function() {
    	console.log("disconnected")
    });
    socket.on('json', function(data) {
    	console.log('im getting new product info');
    	var product = data;
    	if (product) {
    		display_just_scanned(product);
    		display_product_info(product)
    	}
    });

});

function display_just_scanned(product) {
	var urlForImage;

	urlForImage = "/static/" + product["img-url"];
	productImage.attr("src", urlForImage)
}

function display_product_info(product) {
	product_html = construct_product_html(product);
	productList.append(product_html);
};

function construct_product_html(product) {
	product_html_string = '<div class="product-row">' +
	    '<div class="product-name col-md-10">'+product.name+'</div>' + 
	    '<div class="product-price col-md-2">'+product.price+'</div></div>';
	return product_html_string
};
