        $(function(e){

            function tracking(e, data){
                document.getElementById('event').innerHTML = e.type + '.'+ e.namespace
                if(data){
                    document.getElementById('cls').innerHTML = data.config.cls
                    document.getElementById('drag_old').innerHTML = data.config.drag_old
                    document.getElementById('horizontal-track').innerHTML = data.config.horizontal
                    document.getElementById('start').innerHTML = data.config.start
                    document.getElementById('step').innerHTML = data.config.step

                    document.getElementById('selector').innerHTML = e.currentTarget.className

                    document.getElementById('scrollHeight').innerHTML = data.tracking.scrollHeight == undefined ? data.tracking.scrollWidth : data.tracking.scrollHeight
                    document.getElementById('paneHeight').innerHTML = data.tracking.paneHeight == undefined ? data.tracking.paneWidth : data.tracking.paneHeight
                    document.getElementById('dragHeight').innerHTML = data.tracking.dragHeight == undefined ? data.tracking.dragWidth : data.tracking.dragHeight
                    document.getElementById('dragTop').innerHTML = data.tracking.dragTop == undefined ? data.tracking.dragLeft : data.tracking.dragTop
                    document.getElementById('dragBot').innerHTML = data.tracking.dragBot == undefined ? data.tracking.dragRight : data.tracking.dragBot
                }

                return true;
            }
            $('body').on({
                'scrolling.load':function(e, data){
                    tracking(e, data)
                },
                'scrolling.mouseenter': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.mouseleave': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.left': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.right': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.top': function (e, data) {
                    tracking(e, data)
                    $('.top.red').stop(false, true).fadeIn().delay(500).fadeOut()
                },
                'scrolling.bottom': function (e, data) {
                    tracking(e, data)
                    $('.bottom.red').stop(false, true).fadeIn().delay(500).fadeOut()
                },
                'scrolling.mouseover': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.scroll': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.create': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.mousemove': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.mousedown': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.mouseup': function (e, data) {
                    tracking(e, data)
                },
                'scrolling.loaded': function (e, data) {
                    tracking(e, data)
                }
            }, '.scroll, .scroll-old, .scroll-step, .scroll-horizontal, .scroll-button'); //tracking(e, data);

            new Scroll({
                horizontal:true
            });
             return true;
        });
	menu_visible = false;
	$(function(){
		$('#menubutton').click(function(){
			if (menu_visible){
				$('#menu').removeClass('visible').addClass('hidden');
				menu_visible = !menu_visible;
				}
			else {
				$('#menu').removeClass('hidden').addClass('visible');
				menu_visible = !menu_visible;
			}
		});
	});