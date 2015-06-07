var paint = null;
var brush = null;

function initEditor() {
	var layerButtons = document.querySelector('.layers').children;
	
	// Настройка редактора
	paint = new Paint(canvas, {
		wacom_plugin: null,//TODO: wtPlugin, //я забыл, как его подключать...
		layer_numb: 3, //R U HAPPY NOW?
		onLayerChange: function(old_id, cur_id) { //TODO: а зачем оно в параметрах?
			var old = layerButtons[old_id];
			var cur = layerButtons[cur_id];
			old.classList.remove("selected");
			cur.classList.add("selected");
		}
	})
	
	paint.onHistoryStateUpdate = function(eventName) {
		redoAllBut.style.display = paint.canRedo() ? null : 'none'
	}
	
	paint.forEachLayer(function(id, buf) {
		var lb = layerButtons[id]
		if (id == paint.layer_id) lb.classList.add('selected')
		lb.onclick = function(){ paint.layer_id = id }
		layerButtons[id].prependChild(buf)
	})
	
	
	// Настройка инструментов
	brush = new Brush(paint);
	brush.size = 5;
	paint.toolAdd("brush", brush.asBrush());
	paint.toolAdd("eraser", brush.asEraser());
	
	var picker = new Picker(paint);
	paint.toolAdd("picker", picker);
	picker.onColorPick = function(){ var c=this.RGB3f; cp.setRGB(c[0], c[1], c[2], false) }
	
	merge = new Merge(paint);
	paint.toolSet("brush");
	
	/*var img_transf = new ImageTransformer(paint);
	img_transf.setImage(img_for_paint_first_layer);
	paint.toolAdd("image-transform", img_transf);
	paint.toolSet("image-transform");
	//убирает первый шаг истории, в данном случае - появление трансформера, т.е. делает его неубираемым
	paint.history.shift();*/
	
	
	// Настройка цветовыбиралки
	var cp = new ColorPicker(paletteWrap, "static/paint/color_picker_2.0/");
	cp.setRGB(0,0,0);
	cp.onchange = function() {
		brush.colorHTML = this.getHTML();
		ss.color = this.getHTML();
		ob.color = this.getHTML();
	};
	cp.onfinalchange = function() {
		//updateBrushDemo();
	};
	
	
	// Настройка выбиралок блюра, размера, прозрачности
	function updateBrushDemo(rc, w, h) {
		for (var x=w/4; x<w*3/4; x+=brush.step)
			brush.drawDot(rc, x, h/2+Math.cos(x/w*15)*5, 1);
	}
	
	function drawMarker(rc, x, y) {
		rc.fillStyle = "black";
		rc.circleFill(x,y,5);
		rc.circleStroke(x,y,5);
	}
	
	var ob = new OpNBlurSlider(opNBlurSlider, drawMarker, function(x,y) {
		brush.blur = x;
		brush.alpha = y;
	});
	ob.afterUpdate = updateBrushDemo;
	var ss = new SizeSlider(sizeSlider, drawMarker, function(x) {
		brush.size = x*14+2.1;
		ob.update();
	});
	
	
	// Настройка интерфейсных кнопок
	function setTool(name) {
		paint.toolSet(name)
		$('.tool.selected') && $('.tool.selected').classList.remove('selected')
		$('#'+ name +'But').classList.add('selected')
	}
	brushBut.onclick = setTool.bind(null, 'brush')
	eraserBut.onclick = setTool.bind(null, 'eraser')
	pickerBut.onclick = setTool.bind(null, 'picker')
	
	undoBut.onclick = function(){ paint.undo() }
	redoBut.onclick = function(){ paint.redo() }
	redoAllBut.onclick = function(e){ e.stopPropagation(); paint.redoAll(paint.layer_id) }
	
	magicBut.onclick = function(){ merge.drawCurrentLayerOn(0) }
	
	
	// Настройка хоткеев
	document.addEventListener('keyup', function(e){
		switch (e.keyCode) {
		case 90: //'Z'
			paint.undo();
			e.preventDefault();
			break;
		case 89: //'Y'
			paint.redo();
			e.preventDefault();
			break;
		}
	})
}

function SizeSlider(canvas, markerFunc, onChange) {
	var s = this;
	var rc = canvas.getContext('2d');
	var x = 0;
	var color = 'black';
	
	function update() {
		canvas.autoresize();
		var w = canvas.offsetWidth;
		var h = canvas.offsetHeight;
		rc.clear();
		
		rc.lineWidth = 2;
		rc.lineCap = "round";
		rc.strokeStyle = "lightgray";
		rc.line(h/2, h/2, w-h/2, h/2);
		
		rc.fillStyle = color;
		rc.circleFillAndStroke(h/2, h/2, 5);
		rc.circleFillAndStroke(w-h/2, h/2, 15);
		
		markerFunc(rc, x, h/2);
	}
	
	function move(_x) {
		var w = canvas.offsetWidth;
		var h = canvas.offsetHeight;
		var from=h, to=w-h;
		x = toRange(from, _x, to);
		update();
		onChange((x-from)/(to-from));
	}
	control.singleMove({
		move: function(x,y){ move(x); return true },
		elem: canvas
	});
	
	this.update = update;
	Object.defineProperty(this, 'color', {set: function(v){ color = v; update() }});
	move(0);
}

function OpNBlurSlider(canvas, markerFunc, onChange) {
	var s = this;
	var rc = canvas.getContext('2d');
	var x = 0, y = 0;
	var color = 'black';
	var border = 38, hb = border/2; // half-border
	
	function update() {
		canvas.autoresize();
		var w = canvas.offsetWidth;
		var h = canvas.offsetHeight;
		rc.clear();
		
		rc.lineWidth = 2;
		rc.lineCap = "round";
		rc.strokeStyle = "lightgray";
		rc.lines(hb,hb, hb,h-hb, w-hb,h-hb);
		
		rc.fillStyle = color;
		rc.globalAlpha = 0.5;
		rc.circleFillAndStroke(hb, hb, 10);
		rc.globalAlpha = 1;
		
		rc.circleFillAndStroke(hb, h-hb, 10);
		
		rc.shadowBlur = 5;
		rc.shadowOffsetX = -w;
		rc.shadowColor = rc.fillStyle;
		rc.circleFill(w+w-hb, h-hb, 11);
		rc.shadowColor = rc.strokeStyle;
		rc.circleStroke(w+w-hb, h-hb, 10);
		rc.shadowBlur = 0;
		
		if (s.afterUpdate) s.afterUpdate(rc, w, h);
		markerFunc(rc, x, y);
	}
	
	function move(_x, _y) {
		var w = canvas.offsetWidth;
		var h = canvas.offsetHeight;
		x = toRange(border, _x, w-border);
		y = toRange(border, _y, h-border);
		update();
		onChange((x-border)/(w-2*border), (y-border)/(h-2*border));
	}
	control.singleMove({
		move: function(x,y){ move(x,y); return true },
		elem: canvas
	});
	
	this.update = update;
	Object.defineProperty(this, 'color', {set: function(v){ color = v; update() }});
	move(0,9001);
}
