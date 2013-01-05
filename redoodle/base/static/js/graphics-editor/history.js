function History(paintObj) {
	var h=this;
	h.paint=paintObj;
	
	h.historyLen=0;//текущая длина истории (учитывая undo)
	h.step=[];//массив шагов
	h.Step=function(path) {
		var s=this;
		s.region=[];//массив из getImageData
		s.regionPos=[];//массив параметров прямоугольников в верхнем массиве [x0,y0,w0,h0, x1,y1,w1,h2, ...]
		s.path=path;//[[параметры], [собственно путь]]
		
		//устанавливает слой
		s.setLayer=function(layer) {
			this.path[0][0]=layer;
		}
		//для какого слоя тут данные
		s.getLayer=function() {
			return this.path[0][0];
		}
		//возвращает площадь i-го прямоугольника
		s.getSquare=function(i) {
			var rp=this.regionPos;
			return rp[i+2]*rp[i+3];
		}
		//возвращает площать прямоугольника, который содержит оба
		//переданных прямоугольника (выбирает минимальный естественно)
		s.getMergedSquare=function(i1,i2) {
			var l,t,r,b, rp=this.regionPos;
			l=Math.min(rp[i1  ], rp[i2  ]);
			t=Math.min(rp[i1+1], rp[i2+1]);
			r=Math.max(rp[i1  ]+rp[i1+2], rp[i2  ]+rp[i2+2]);
			b=Math.max(rp[i1+1]+rp[i1+3], rp[i2+1]+rp[i2+3]);
			return (r-l)*(b-t);
		}
		//растягивает первый прямоугольник так, чтобы второй полностью был внутри 1го
		s.rectMerge=function(i1,i2) {
			var l,t,r,b, rp=this.regionPos;
			l=Math.min(rp[i1  ], rp[i2  ]);
			t=Math.min(rp[i1+1], rp[i2+1]);
			r=Math.max(rp[i1  ]+rp[i1+2], rp[i2  ]+rp[i2+2]);
			b=Math.max(rp[i1+1]+rp[i1+3], rp[i2+1]+rp[i2+3]);
			rp[i1  ]=l;
			rp[i1+1]=t;
			rp[i1+2]=r-l;
			rp[i1+3]=b-t;
		}
		//добавление участка (буфер, размеры области)
		s.add=function(buf,left,top,right,bottom) {
			if (left<0) left=0;
			if (top<0) top=0;
			if (right>buf.width) right=buf.width;
			if (bottom>buf.height) bottom=buf.height;
			if (left>=right || top>=bottom) return; //за пределами канваса или пустой
			
			var w=right-left, h=bottom-top;
			var rc=buf.rc, rp=this.regionPos;
			rp.push(left,top,w,h);
			
			//*-----*    *-------*
			//|  A  |    |       |
			//|   *---*  |  C - -|
			//*---| B |  |   |   |
			//    *---*  *-------*
			//если площадь A+B>C, выгоднее прямоугольники A и B заменить на один C. это и делается
			for (var i=4;i<rp.length;i+=4) {
				if (rp[i]===undefined) alert("");
				for (var j=0;j<i;j+=4) {
					if (rp[j]===undefined) alert("");
					var t1=this.getSquare(i)+this.getSquare(j);
					var t2=this.getMergedSquare(i,j);
					if (t1>t2) {
						this.rectMerge(i,j);
						rp.splice(j,4);
						i-=4;
						j-=4;
					}
				}
			}
		}
		//проход по массиву прямоугольников, копирование пикселов
		s.capture=function(buf) {
			this.region=[];
			var rc=buf.rc, rp=this.regionPos;
			for (var i=0;i<rp.length;i+=4) {
				this.region.push(rc.getImageData(rp[i],rp[i+1],rp[i+2],rp[i+3]));
				//rc.strokeRect(rp[i],rp[i+1],rp[i+2],rp[i+3]);
			}
		}
		//восстановление пикселов
		s.restore=function(buf) {
			var rc=buf.rc, rp=this.regionPos;
			for (var i=0;i<this.region.length;i++) {
				rc.putImageData(this.region[i],rp[i*4],rp[i*4+1]);
			}
		}
		
		s.paintRestore=function(paint) {
			paint.onRestorePath(this.path);
		}
		return s;
	}
	
	h.StepMerge=function(src_layer) {
		var s=this;
		s.src_layer=src_layer;
		s.dest_layer=null;
		s.data=null;
		
		//устанавливает слой
		s.setLayer=function(dest_layer) {
			this.dest_layer=dest_layer;
		}
		//для какого слоя тут данные
		s.getLayer=function() {
			return this.dest_layer;
		}
		s.restore=function(dest_buf) {
			dest_buf.rc.putImageData(this.data,0,0);
		}
		s.capture=function(dest_buf) {
			this.data=dest_buf.rc.getImageData(0,0, dest_buf.width,dest_buf.height);
		}
		s.paintRestore=function(paint) {
			paint.onRestoreMerge(this.dest_layer,this.src_layer);
		}
	}
	
	
	h.add=function(newStep) {
		if (this.historyLen!=this.step.length)
			this.step.splice(this.historyLen, this.step.length-this.historyLen);
		this.step.push(newStep);
		this.historyLen++;
	}
	
	//добавление
	// * канвас, который (возможно) будет скопирован
	// * путь - массив [[слой,размер кисти,размытие кисти,...],[x0,y0,x1,y1,...]]
	h.addPath=function(buffer_array,path,r) {
		var s=new this.Step(path);
		var params=path[0];
		path=path[1];
		if (path.length==0) return;
		var layerId=params[0];
		var buf=buffer_array[layerId];
		//var r=Math.ceil(params[1]/2+params[2]*1.5);
		
		var left=path[0],top=path[1],right=path[0],bottom=path[1];
		for (var i=3;i<path.length;i+=3) {
			var x=path[i], y=path[i+1];
			if (left>x) left=x;
			if (right<x) right=x;
			if (top>y) top=y;
			if (bottom<y) bottom=y;
			var square=(right-left)*(bottom-top);
			if (i<path.length-3	&& square>64*64) {
				s.add(buf,left-r,top-r,right+r,bottom+r);
				left=path[i]; top=path[i+1];
				right=path[i];bottom=path[i+1];
			}
		}
		s.add(buf,left-r,top-r,right+r,bottom+r);
		s.capture(buf);
		
		this.add(s);
	}
	
	h.addMerge=function(buf_array,dest_id,src_id) {
		var s=new this.StepMerge(src_id);
		s.setLayer(dest_id);
		s.capture(buf_array[dest_id]);
		this.add(s);
	}
	
	//получает массив слоёв, выбирает нужный,
	//восстанавливает участки в него
	h.undo=function(buffer_array) {
		if (this.historyLen==0) return;
		this.historyLen--;
		var s=this.step[this.historyLen];
		var layerId=s.getLayer();
		s.restore(buffer_array[layerId]);
	}
	//если передан номер слоя, делает redo в слой с этим номером
	//иначе - в слой, записанный в параметрах
	h.redo=function(forceLayer) {
		if (this.historyLen==this.step.length) return false;
		var s=this.step[this.historyLen++];
		if (forceLayer!==undefined) {
			s.setLayer(forceLayer);
			s.capture(this.paint.layer[forceLayer]);
		}
		s.paintRestore(this.paint);
		return true;
	}
	
	return h;
}


/*
function createHistory() {
	var h=new Object();
	
	h.layer=[];//слои. храним для каждого все пути и немного кейфреймов
	h.snapshotStep=10;//шаг кейфреймов
	h.historyLen=0;//текущая длина истории (учитывая undo)
	h.layerHistory=[];
	h.createLayer=function() {
		l=new Object();
		l.path=[];
		l.snapshot=[];
		return l;
	}
	h.initLayers=function(w,h,numb) {
		for (var i=0;i<numb;i++)
			this.layer[i]=this.createLayer();
	}
	//добавление
	// * номер слоя
	// * путь - массив [x0,y0,x1,y1,...]
	// * канвас, который (возможно) будет скопированч
	h.add=function(layer_id,path,buffer) {
		var l=this.layer[layer_id];
		var cacheLen=l.path.length;
		
		if (this.historyLen!=cacheLen) {
			l.path.splice(0,this.historyLen);
			l.snapshot.splice(0,Math.ceil(this.historyLen/this.snapshotStep));
		}
		
		if (l.path.length%this.snapshotStep==0) {
			l.snapshot.push(
				buffer.rc.getImageData(0,0,buffer.width,buffer.height));
		}
		l.path.push(path.slice());
		this.historyLen++;
	}
	
	h.undo=function()
	
	return h;
}
*/