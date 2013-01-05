//TODO: (test) buffer layers to one
//TODO: total radius to params

//создаёт канвас. работает как буффер для рисования
function createBuffer(w, h) {
	h || (h=w);//если не указан 2й параметр,
	           //делаем квадратный
	var buffer = document.createElement('canvas');
	buffer.rc=buffer.getContext("2d");
	buffer.width = w;
	buffer.height = h;
	return buffer;
}

//прямоугольник
function Rect() {
	this.reset=function(x,y,r) {
		if (x===undefined || y===undefined || r===undefined) {
			this.x0=+Infinity;//(x0,y0)----*
			this.y0=+Infinity;//   |       |
			this.x1=-Infinity;//   |       |
			this.y1=-Infinity;//   *----(x1,y1)
		} else {
			this.x0=x-r;
			this.x1=x+r;
			this.y0=y-r;
			this.y1=y+r;
		}
	}
	this.extend=function(x,y,r) {
		if (this.x0>x-r) this.x0=x-r;
		if (this.x1<x+r) this.x1=x+r;
		if (this.y0>y-r) this.y0=y-r;
		if (this.y1<y+r) this.y1=y+r;
	}
	this.reset();
	/*if (arr)
		for (var i=0;i<arr.length;i+=2)
			this.extend(arr[i],arr[i+1]);*/
	return this;
}

//создаёт объект рисовальщика, завязан на canvas'е
function Paint(canvas) {
	var p=this;
	p.rc=canvas.getContext("2d");
	p.width=canvas.width;
	p.height=canvas.height;
	p.buffer=createBuffer(p.width,p.height);
	
	
	//просто линия между точками
	p.line=function(rc,x0,y0,x1,y1) {
		rc.beginPath();
		rc.moveTo(x0,y0);
		rc.lineTo(x1,y1);
		rc.stroke();
	}
	//просто круг с координатами и радиусом
	p.circle=function(rc,x,y,r) {
		rc.beginPath();
		rc.arc(x,y, r, 0,3.1415927*2, false);
		rc.stroke();
	}
	
	
	
	//параметры и методы кисти
	p.brushColor=['#000000',1];
	p.brushSetColor=function(c) {
		this.brushColor[0]=c;
		this.brushSpriteUpdate();
	}
	p.brushGetColor=function() {
		return this.brushColor[0];
	}
	p.brushSetAlpha=function(a) {
		this.brushColor[1]=a;
	}
	p.brushSize=0;
	p.brushSizeMax=32;
	p.brushBlur=1;
	p.brushBlurMax=16;
	p.brushStep=2;
	p.brushBuffer=createBuffer(p.brushSizeMax+2);
	p.brushSpriteBlurStretch=1.25;//на сколько увеличивается bounding box кисти при увеличении блюра на 1 (с запасом)
	p.brushSprite=createBuffer(p.brushSizeMax+p.brushBlurMax*p.brushSpriteBlurStretch*2);
	//полный радиус кисти. по сути - ребро bounding box'а пополам
	p.brushGetTotalRadius=function() {
		return this.brushSize*0.5+Math.max(this.brushBlur*this.brushSpriteBlurStretch,2);
	}
	//перерисовываем спрайт кисти
	p.brushSpriteUpdate=function() {
		var buf=this.brushSprite, brc=buf.rc;
		brc.clearRect(0,0,buf.width,buf.height);
		brc.shadowBlur=this.brushBlur;
		brc.shadowOffsetX=this.brushSizeMax*3;
		brc.shadowColor=this.brushColor[0];
		brc.beginPath();
		var dx=this.brushGetTotalRadius();
		brc.arc(dx-brc.shadowOffsetX,dx, this.brushSize*0.5, 0,3.1415927*2, false);
		brc.fill();
	}
	//меняем силу разблюра
	p.brushSetBlur=function(blur) {
		if (blur>this.brushBlurMax) blur=this.brushBlurMax;
		if (blur<0) blur=0;
		this.brushBlur=blur;
		this.brushSpriteUpdate();
	}
	//устанавливает размер кисти
	p.brushSetSize=function(size) {
		if (size>this.brushSizeMax) size=this.brushSizeMax;
		if (size<1) size=1;
		this.brushSize=size;
		//this.getLayerBuffer().rc.lineWidth=size;//зачем это здесь?
		
		//рисуем кружок кисти в буффер, потом будет рисовать этот буффер под мышкой
		//отрисовка буффера проходит быстрее, чем отрисовка 2х кругов, в ~10 раз
		var buf=this.brushBuffer, brc=buf.rc;
		brc.clearRect(0,0,buf.width,buf.height);
		
		brc.strokeStyle="white";
		brc.lineWidth=3;
		this.circle(brc, buf.width*0.5,buf.height*0.5, size*0.5);
		
		brc.strokeStyle="black";
		brc.lineWidth=1;
		this.circle(brc, buf.width*0.5,buf.height*0.5, size*0.5);
		
		this.brushSpriteUpdate();
	}
	//возвращает размер кисти
	p.brushGetSize=function() {
		return this.brushSize;
	}
	
	
	//рисует линию спрайтом
	p.brushLine=function(x0,y0,x1,y1,p0,p1) {
		var rc=this.buffer.rc;
		rc.globalAlpha=this.brushColor[1];
		var d=this.brushGetTotalRadius(), dr;
		var d2=d*2, d2r;
		//x0-=d; y0-=d; x1-=d; y1-=d;
		var s;
		var k, dx=x1-x0, dy=y1-y0, len=Math.sqrt(dx*dx+dy*dy), dp=p1-p0,
			adx=Math.abs(dx), ady=Math.abs(dy);
		var step;
		//step=len/Math.ceil(len/step);
		if (adx>ady) {
			step=this.brushStep/len*adx;
			k=dy/dx;
			if (dx>0) s=1; else s=-1;
			for (var i=0;i<=adx;i+=step) {
				dr=(p0+dp*i/adx)*d; d2r=dr*2;
				rc.drawImage(this.brushSprite, 0,0,d2,d2, x0+i*s-dr,y0+i*k*s-dr, d2r,d2r);
			}
		} else {
			step=this.brushStep/len*ady;
			k=dx/dy;
			if (dy>0) s=1; else s=-1;
			for (var i=0;i<=ady;i+=step) {
				dr=(p0+dp*i/ady)*d; d2r=dr*2;
				rc.drawImage(this.brushSprite, 0,0,d2,d2, x0+i*k*s-dr,y0+i*s-dr, d2r,d2r);
			}
		}
		rc.globalAlpha=1;
	}
	//рисует точку спрайтом
	p.brushDot=function(x,y,pressure) {
		var rc=this.buffer.rc;
		rc.globalAlpha=this.brushColor[1];
		var d=this.brushGetTotalRadius(), dr=d*pressure;
		var d2=d*2, d2r=d2*pressure;
		rc.drawImage(this.brushSprite, 0,0,d2,d2, x-dr,y-dr,d2r,d2r);
		rc.globalAlpha=1;
	}
	
	
	
	//параметры и методы слоёв
	p.layer=[];//массив слоёв (объектов canvas)
	p.layer_numb=4;//количество слоёв
	for (var i=0;i<p.layer_numb;i++)//каждому слою по буфферу
		p.layer.push(createBuffer(p.width,p.height));
	p.layer_cur=0;//текущий
	p.getLayerBuffer=function(id) {//возвращает буффер узананного слоя (текущий по умолчанию)
		if (id===undefined) return this.layer[this.layer_cur];
		//if (id<0 || id>=this.layer_numb) return null;
		return this.layer[id];
	}
	p.setLayer=function(id) {//переключается на слой, устанавливает ему параметры
		if (id>=this.layer_numb) id=this.layer_numb-1;
		if (id<0) id=0;
		this.layer_cur=id;
	}
	
	p.autoUpdate=true;//автоматическая перерисовка при рисовании чего-то (отключается при восстановлении из истории)
	//обновляет всё (если указаны координаты, нарисуется кружок кисти)
	p.refresh=function(mouse_x,mouse_y) {
		this.refreshRegion(0,0,this.width,this.height,mouse_x,mouse_y);
	}
	//обновляет прямоугольную область
	p.refreshRegion=function(x,y,w,h,mouse_x,mouse_y) {
		this.rc.clearRect(x,y,w,h);
		for (var i=0;i<=this.layer_cur;i++)//всё, что ниже временного слоя
			this.rc.drawImage(this.layer[i], x,y,w,h, x,y,w,h);
			
		this.rc.drawImage(this.buffer, x,y,w,h, x,y,w,h);//временный слой
		
		for (var i=this.layer_cur+1;i<this.layer_numb;i++)//всё, что выше временного
			this.rc.drawImage(this.layer[i], x,y,w,h, x,y,w,h);
		
		if (mouse_x!==undefined && mouse_y!==undefined) {
			var d=this.brushBuffer.width*0.5;
			this.rc.drawImage(this.brushBuffer,mouse_x-d,mouse_y-d);//кружок радиуса кисти
		}
	}
	//обновляет прямоугольную область, расширяемую радиусом. проверяет на выход за границы канваса
	p.refreshRegionCoords=function(x0,y0,x1,y1,r,mouse_x,mouse_y) {
		if (x0<x1) {w=x1-x0;} else {w=x0-x1; x0=x1;}
		if (y0<y1) {h=y1-y0;} else {h=y0-y1; y0=y1;}
		x0=Math.floor(x0-r);
		y0=Math.floor(y0-r);
		w=Math.ceil(w+r*2);
		h=Math.ceil(h+r*2);
		if (x0<0) x0=0;
		if (y0<0) y0=0;
		if (x0+w>this.width) w=this.width-x0;
		if (y0+h>this.height) h=this.height-y0;
		if (w<=0 || h<=0) return;
		this.refreshRegion(x0,y0,w,h,mouse_x,mouse_y);
	}
	
	p.brushLeft=0;//через сколько пикселов начинать новый отрезок
	p.lastX=0;//TODO: use path
	p.lastY=0;
	p.lastPressure=1;
	p.refreshRect=new Rect();
	p.isDrawing=false;//идёт ли сейчас рисование
	p.path=[];//путь (или полоса). массив вида [x0,y0,pressure0, x1,y1,pressure1, ...]
	p.params=[];//параметры [слой,размер,блюр,шаг,цвет,форма]
	p.frameDelta=16;//ограничение кол-ва обновлений канваса в секунду (FPS=1000/frameDelta)
	p.lastFrameTime=0;//время последнего обновления канваса
	//начало рисования штриха
	p.start=function(x,y,pressure) {
		if (this.historyEnabled) {
			this.params=this.getParams();
			this.path=[x,y,pressure];
		}
		
		this.brushDot(x,y,pressure);
		this.brushLeft=this.brushStep;
		this.isDrawing=true;
		if (this.autoUpdate) {
			var r=this.brushGetTotalRadius();
			this.refreshRegionCoords(x,y, x,y, r,x,y);
			this.refreshRect.reset(x,y,r);
			this.lastFrameTime=new Date().getTime();
		}
		this.lastX=x;
		this.lastY=y;
		this.lastPressure=pressure;
	}
	//шаг рисования
	p.move=function(x,y,pressure) {
		if (this.isDrawing) {
			if (this.historyEnabled)
				this.path.push(x,y,pressure);
			
			var dx=x-this.lastX, dy=y-this.lastY, len=Math.sqrt(dx*dx+dy*dy), dp;
			//console.log("START len: "+len+" left:"+this.brushLeft+
			//            "("+this.lastX+","+this.lastY+") - ("+x+","+y+")");
			if (len>this.brushLeft) {
				dx*=this.brushLeft/len;
				dy*=this.brushLeft/len;
				dp=(pressure-this.lastPressure)*this.brushLeft/len;
				this.brushLine(this.lastX+dx,this.lastY+dy, x,y, this.lastPressure+dp,pressure);
				this.brushLeft=this.brushStep-(len-this.brushLeft)%this.brushStep;
				//console.log("line ("+(this.lastX+dx)+","+(this.lastY+dy)+")");
			} else if (len==this.brushLeft) {
				this.brushDot(x,y,pressure);
				this.brushLeft=this.brushStep;
				//console.log("dot");
			} else {
				this.brushLeft-=len;
				//console.log("skip");
			}
			//console.log("END len: "+len+" left: "+this.brushLeft);
		}
		if (this.autoUpdate) {
			var r=this.brushGetTotalRadius();
			var ct=new Date().getTime();
			this.refreshRect.extend(x,y,r);
			if (ct-this.lastFrameTime>this.frameDelta) {
				var rect=this.refreshRect;
				this.refreshRegionCoords(rect.x0,rect.y0, rect.x1,rect.y1, r,x,y);
				rect.reset(x,y,r);
				this.lastFrameTime=ct;
			}
		}
		this.lastX=x;
		this.lastY=y;
		this.lastPressure=pressure;
	}
	p.end=function() {
		if (!this.isDrawing) return;
		if (this.historyEnabled)
			this.history.addPath(this.layer,[this.getParams(),this.path],this.brushGetTotalRadius());
		this.getLayerBuffer().rc.drawImage(this.buffer,0,0);//TODO: draw only changed
		this.buffer.rc.clearRect(0,0,this.buffer.width,this.buffer.height);
		this.isDrawing=false;
		
		//for speed comparison
		var dt=new Date().getTime()-this.lastFrameTime;
		var l=0;
		for (var i=3;i<this.path.length;i+=3) {
			var dx=this.path[i]-this.path[i-3], dy=this.path[i+1]-this.path[i-2];
			l+=Math.sqrt(dx*dx+dy*dy);
		}
		return [l/dt,this.path.length/dt];
	}
	
	p.merge=function(src_buf_id) {
		if (this.historyEnabled)
			this.history.addMerge(this.layer,this.layer_cur,src_buf_id);
		this.layer[this.layer_cur].rc.drawImage(this.layer[src_buf_id], 0,0);
		this.refresh();
	}
	
	
	p.undo=function() {
		if (!this.historyEnabled) return;
		this.history.undo(this.layer);
		this.refresh();
	}
	p.redo=function() {
		if (!this.historyEnabled) return;
		this.history.redo();
		this.refresh();
	}
	p.redoAll=function(forceLayer) {
		if (!this.historyEnabled) return;
		while (this.history.redo(forceLayer)) {};
		this.refresh();
	}
	//вызываемая извне(например, из истории) функция, отрисовывающая путь
	//путь - [[слой,размер,блюр,полный радиус,шаг,цвет,форма,режим],[x0,y0,p0, x1,y1,p1, ...]]
	p.onRestorePath=function(path) {
		var _p=this.getParams();
		this.setParams(path[0]);
		path=path[1];
		
		this.historyEnabled=false;
		this.autoUpdate=false;
		this.start(path[0],path[1],path[2]);
		for (var i=3;i<path.length;i+=3) {
			this.move(path[i],path[i+1],path[i+2]);
		}
		this.end();
		this.setParams(_p);
		this.historyEnabled=true;
		this.autoUpdate=true;
		
		this.refresh();
	}
	p.onRestoreMerge=function(dest_buf_id,src_buf_id) {
		this.historyEnabled=false;
		var t=this.layer_cur;
		this.layer_cur=dest_buf_id;
		
		this.merge(src_buf_id);
		
		this.layer_cur=t;
		this.historyEnabled=true;
		
		this.refresh();
	}
	
	//упаковка всех текущих параметров в массив
	p.getParams=function() {
		var _p=[this.layer_cur,this.brushSize,this.brushBlur,
		        this.brushStep,this.brushColor.slice(),0,0];
		return _p;
	}
	//восстановление параметров из массива
	p.setParams=function(_p) {
		this.setLayer(_p[0]);
		this.brushSetSize(_p[1]);
		this.brushSetBlur(_p[2]);
		this.brushStep=_p[3];
		this.brushColor=_p[4];
		//,0=_p[5];
		this.brushSpriteUpdate();
	}
	
	p.historyEnabled=true;
	p.history=new History(p);
	
	
	p.brushSetSize(5);
	p.setLayer(0);
	
	return p;
}