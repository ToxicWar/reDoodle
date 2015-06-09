$ = document.querySelector.bind(document);
$$ = document.querySelectorAll.bind(document);
Element.prototype.$ = Element.prototype.querySelector
Element.prototype.$$ = Element.prototype.querySelectorAll
Element.prototype.prependChild = function(elem){
	this.insertBefore(elem, this.firstChild);
}

function send_image(canvas) {
	var base64 = canvas.toDataURL();
	var xhr = new XMLHttpRequest();
	xhr.open('POST', "/save_image/");
	var formData = new FormData();
	formData.append('base64', base64);
	formData.append('room', currRoom.id);
	formData.append('chain', currChain.name);
	xhr.onreadystatechange = function() {
		if (xhr.readyState != 4) return;
		alert("ok")
	}
	xhr.send(formData);
}

function like(chain, like) {
	var xhr = new XMLHttpRequest();
	var formData = new FormData();
	formData.append('chain', chain.name);
	formData.append('like', like ? '1' : '0');
	console.log(like, like ? '1' : '0')
	xhr.open('POST', "/like_chain/");
	xhr.onload = function() {
		var new_amount = +xhr.responseText
		var elem = document.getElementById(chain.id+"like").previousSibling
		elem.textContent = new_amount
	}
	xhr.send(formData);
}
