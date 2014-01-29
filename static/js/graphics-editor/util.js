function getPos(obj) {
	var curleft = curtop = 0;
	if (obj.offsetParent)
		do {
			curleft += obj.offsetLeft;
			curtop += obj.offsetTop;
		} while (obj = obj.offsetParent);
	return [curleft,curtop];
}

function col2rgb(str) {
	rgb=[];
	for (var i=1;i<7;i+=2) rgb.push(parseInt(str.substring(i,i+2),16));
	return rgb;
}
function rgb2col(arr) {
	str="#";
	for (i in arr) str+=arr[i]>15 ? arr[i].toString(16) : "0"+arr[i].toString(16);
	return str;
}
