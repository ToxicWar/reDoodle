var userID;
//temp:
param={};
var OCcanvas, OCCcontext, Scanvas, SCcontext;
var ROOMSDATA = {}; // id&name
hightFix = 0;

contentHeight = 515;
//кашка картинок
like =  new Image();
like.src="http://i.imgur.com/fQnBe0a.png"
//кашка кончилась
function init(){
/*
	VK.init(function() {
		 // API initialization succeeded
		 // Your code here
		
		VK.addCallback('onScrollTop', function(scrollTop, VKwindowHeight, VKpaddingTop){
										headSize = head.offsetHeight;
										if (VKwindowHeight < 500) return;
										content.style.height = VKwindowHeight - headSize - 16 +"px";
										contentHeight = content.offsetHeight;
										VK.callMethod("resizeWindow", 980, content.offsetHeight + headSize + 16); 
										VK.callMethod("scrollWindow", VKpaddingTop, 200)
									  })
		VK.addCallback('onScroll', function(scrollTop, VKwindowHeight){
										headSize = head.offsetHeight;
										if (VKwindowHeight < 500) return;
										content.style.height = VKwindowHeight - headSize - 16 +"px";
										contentHeight = content.offsetHeight;
										VK.callMethod("resizeWindow", 980, content.offsetHeight + headSize + 16); 
									  })							  
		VK.callMethod('scrollTop'); 
		VK.callMethod('scrollSubscribe',true); 
		main();
	});
	//VK.callMethod("setTitle","reDoodle") вид: Вконтакте/Редудл
	//VK.callMethod("resizeWindow", 510, 600); 
*/
	if(document.getElementById("opnsoapc")){
		OCcanvas = document.getElementById("opnsoapc");
		OCCcontext = OCcanvas.getContext('2d');
		OCcanvas.addEventListener('click', function(evt) {
			//mouse = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;
			dot(OCcanvas, getMousePos(OCcanvas, evt));
		}, false);
		dot(OCcanvas)
	}
	if(document.getElementById("Csize")){
		Scanvas = document.getElementById("Csize");
		SCcontext = Scanvas.getContext('2d');
		Scanvas.addEventListener('click', function(evt) {
			//mouse = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;
			Sdot(Scanvas, getMousePos(Scanvas, evt));
		}, false);
		Sdot(Scanvas)
	}
	
	api_loadRoomsList()
}

function main(){
	whois()
	//document.body.innerHTML = "id " + userID;

}

function whois(){
    d = document.location.search.substr(1);
    var p = d.split("&");
    var V = {}, curr;
    for (i = 0; i < p.length; i++) {
        curr = p[i].split('=');
        V[curr[0]] = curr[1];
    }
    //userID = V['viewer_id']; alert(userID)
	//alert(V['auth_key'])
	//alert(V['hash'])
    //VK.api("users.get", { uid: userID }, function (data) {
    //   alert(data.response[0].last_name + ' ' + data.response[0].first_name);
    //});
}

/********* Head *********/

function logoClick(){
	content.scrollTop = 0
}
function changeRoom(room){
	
}
function addRoom(){
	param.title="Добавить комнату";
	param.content="Введите адрес комнаты: </br><input autofocus name='roomName' id='popUpForm' style='width: 300px;' class='' type='text' /> </br><button>Создать</button>";
	showPopUp(param)
}
function createRoom(){
	param.title="Создать новую комнату"
	param.content="Введите название комнаты: </br><input autofocus name='roomName' id='popUpForm' style='width: 300px;' class='' type='text' /> </br><button onclick='api_addRoom()'>Создать</button>";
	showPopUp(param)
}

/********* room loading content *********/
function api_loadRoomsList(){
	loading.setAttribute("class","visible");
    xmlhttp = new XMLHttpRequest();    
    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
        {
			var income = JSON.parse(xmlhttp.responseText);
			var html = "";
			for (i=0; i<income.results.length; i++){
				html += addRoomIntoList(income.results[i]) //туду: переписать под другую функцию
				ROOMSDATA[income.results[i].id] = income.results[i];
			}
			roomsList.innerHTML = html;
			loading.setAttribute("class","hidden");
			api_load(ROOMSDATA[1])
        }
    }   
    xmlhttp.open('GET', "/api/rooms/", true);
    xmlhttp.send(); 
	
	hightFix = rooms.offsetHeight;
	
	function addRoomIntoList(data){
		result = "<span class='myRoom' onclick='api_load(ROOMSDATA[" + data.id +"])'>"+ data.name + "</span>";
		return result;
	}
}

function api_addRoom(){
	if(popUpForm.value!=""){
		loading.setAttribute("class","visible");
		
		xmlhttp = new XMLHttpRequest();    

		xmlhttp.open('POST', "/api/rooms/", true);
		xmlhttp.setRequestHeader("Content-Type", "application/json");
		data = {"name": popUpForm.value};
		xmlhttp.send(JSON.stringify(data)); 
		setTimeout('api_loadRoomsList()', 300)
	} else {
		hidePopUp()
		param.title="Ошибка"
		param.content="Вы не ввели название комнаты."
		showPopUp(param)
	}
	loading.setAttribute("class","hidden");
}

function addRoomElemToList(roomName, roomId){
	parent = document.getElementById("roomsList");
	roomEl = document.createElement('span');
	roomEl.className = 'myRoom';
    roomEl.addEventListener("click", "load("+ roomId + ")");
	parent.appendChild(roomEl);
}

function api_load(room){
	loading.setAttribute("class","visible");
    xmlhttp = new XMLHttpRequest();    
    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
        {
			document.getElementById("roomName").setAttribute("onclick", "load('" + room.id + "')")
			document.getElementById("roomName").setAttribute("roomId", room.id)
			document.getElementById("roomNameText").innerHTML = "Комната " + room.name +":"
			document.getElementById("roomShare").setAttribute("onclick", "shareRoom('"+ room.id + "')") //TODO vk-format
			document.getElementById("roomAction").setAttribute("onclick", "newChain()")
			document.getElementById("canselEditing").setAttribute("onclick", "load('" + room.id + "')")
			var income = JSON.parse(xmlhttp.responseText);
			//var html = "<div id='newChain' onclick='newChain()'><div style='margin: auto; width: 130px; padding: 11px;'>Создать цепочку</div></div>"; 
			var html = "";
			for (i=0; i<income.chain_set.length; i++){
				html += addChain(income.chain_set[i])
			}
			content.innerHTML = html;
			loading.setAttribute("class","hidden");
			content.setAttribute("class", "")
			scroll(0,0)
        }
    }   
    xmlhttp.open('GET', "/api/rooms/" + room.id, true);
    xmlhttp.send();  

	function addChain(data){
		var images = ""
		for (j=0; j<data.image_set.length; j++){
			images += "<img class='chainPic' src='" + data.image_set[j].image + "'></img>";
		}
		
		return "<div class='chain'><div class='chainName'><div class='name f_l' onclick='shareChain(" +data.id
			  +")'><div class='f_l'>" + data.name
			  +"</div><div class='share f_r'></div></div><div class='likes f_r' onclick='likeChain("+ data.id	
			  +")'><div class='f_l' style='margin-right: 5px'>Понравилось:</div><div class='f_l' style='margin-right: 5px'>" + data.likes
			  +"</div><div class='f_l likeHeart nolike' id='" + data.id
			  +"like'> </div></div></div><div class='chainBody'><div class='columnPic'>" + images
			  +"<div class='continue' onclick='continueChain(" + data.id + ", &#39" + data.name
			  +"&#39)'><div class='textInNaviBut" /* + TODO data.is_blocked */
			  +"'>Продолжить</div></div></div></div><div class='chainFooter'></div></div>"
			   
	}
	
}

/********* pop up content *********/
function newChain(){
	param.title = "Создать новую цепочку";
	param.content="Введите название цепочки: </br><input autofocus name='roomName' id='popUpForm' style='width: 300px;' class='' type='text' /> </br><button>Создать</button>";
	param.room = currRoom;
	showPopUp(param)
}
function shareChain(chain){
	param.title = "Поделиться цепочкой";
	param.content="Скопируйте адрес цепочки: <div id='chainLinkInPopUp'>"+ chain +"</div></br>Или поделитесь вконтакте</br><button>Поделиться</button>";
	param.chain = chain;
	showPopUp(param)
}
function likeChain(chain){
	document.getElementById(chain+"like").setAttribute("class","f_l likeHeart yeslike")
}
function continueChain(chainId, chainName){
//todo спрятать комнаты
	
	rooms.style.display = "none"
	container.style.height = container.offsetHeight + hightFix + "px"
	
	content.setAttribute("class", "editPage")
	content.innerHTML = editorHTML;
	
	roomShare.style.display = "none";
	roomAction.style.display = "none";
	
	editingText.innerHTML = "новая картинка в цепочку " + chainName
	editing.style.display = "block";
	canselEditing.style.display = "block";
	
	editor.style.paddingTop = (container.offsetHeight - 525)/2 +"px"
}
/********* pop up and rooms block hiding *********/
/*
function onContentScroll(){
	if(content.scrollTop > 200) {
		rooms.setAttribute("class", "hidden")
		content.style.height = contentHeight + roomsDivHeight +"px";
	} else {
		content.style.height = contentHeight + "px";
		rooms.setAttribute("class", "visible")
	}
}
*/
function hidePopUp(){
	darkSide.setAttribute("class","hidden");
	popUp.setAttribute("class","hidden");
}
function showPopUp(param){
	darkSide.setAttribute("class","visible");
	popUp.setAttribute("class","visible");
	puTitle.innerHTML = param.title;
	puBody.innerHTML = param.content;
	popUpForm.focus();
	param={};
	
}


/********* editors canvases *********/
function dot(canvas, mousePos){
	
	OCCcontext.clearRect(0, 0, canvas.width, canvas.height);
	
	OCCcontext.beginPath();
	OCCcontext.moveTo(30, 20);
	OCCcontext.lineTo(30, 180);
	OCCcontext.lineTo(190, 180);
	OCCcontext.stroke();

	OCCcontext.beginPath();
	OCCcontext.arc(15, 10, 7, 0, 360, true);
	OCCcontext.stroke();
	
	OCCcontext.beginPath();
	OCCcontext.arc(200,190, 7, 0, 360, true);
	OCCcontext.stroke();
	
	OCCcontext.beginPath();
	if(mousePos===undefined){OCCcontext.arc(30,180, 5, 0, 360, true);} else {
		OCCcontext.arc(mousePos.x, mousePos.y, 5, 0, 360, true);
	}
	OCCcontext.fill();
	OCCcontext.stroke();
	
}

function Sdot(canvas, mousePos){

	SCcontext.clearRect(0, 0, canvas.width, canvas.height);
	
	SCcontext.beginPath();
	SCcontext.moveTo(30, 20);
	SCcontext.lineTo(190, 20);
	SCcontext.stroke();

	SCcontext.beginPath();
	SCcontext.arc(15, 20, 5, 0, 360, true);
	SCcontext.stroke();
	
	SCcontext.beginPath();
	SCcontext.arc(200, 20, 8, 0, 360, true);
	SCcontext.stroke();
	
	SCcontext.beginPath();
	if(mousePos===undefined){SCcontext.arc(30, 20, 5, 0, 360, true);} else {
		SCcontext.arc(mousePos.x, 20, 5, 0, 360, true);
	}
	SCcontext.fill();
	SCcontext.stroke();
	
}
function getMousePos(canvas, evt) {
    rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

 