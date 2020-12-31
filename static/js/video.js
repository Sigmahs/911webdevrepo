const constraints = {
  video: true
};

var face_id = 0;
window.onload=function () {
    face_id = '_' + Math.random().toString(36).substr(2, 9);
    callLimit();
    

};
var loaded= 0;
var snap;

var  starttime;
var endtime;
var limit_reached = 'false';


navigator.mediaDevices.getUserMedia(constraints).
  then((stream) => {
  	var video = document.getElementById('videoElement');
  	video.srcObject = stream;

	 });
	  

function screenshot() {
	


  var d = new Date();
	
	var video = document.getElementById('videoElement');
	var canvas = document.getElementById('screenshot');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  var overlay = document.getElementById('overlay');
  overlay.width = video.videoWidth;
  overlay.height=video.videoHeight;
  
  startime = d.getTime();
	endtime= startime + 10000;
  // Other browsers will fall back to image/png
  
  if (d.getTime() < endtime & limit_reached === 'false') {
  loaded += 1;
  submitCanvasToURL();

  postCanvasToURL();
} else {
  document.getElementById('results_overlay').src = "data:text/html;charset=utf-8," + "<h1 style='color:white'>Usage Limit Reached</h1>";
    
}

}

//size too big error message


function postCanvasToURL() {
  // Convert canvas image to Base64
  var d = new Date();
  var video = document.getElementById('videoElement');
  var canvas = document.getElementById('screenshot');
  canvas.getContext('2d').drawImage(video, 0, 0);

  var img = canvas.toDataURL();
  // Convert Base64 image to binary
  var file = dataURItoBlob(img);

  var formdata = new FormData();
formdata.append( 'avatar', file);
formdata.append('repeat', face_id + loaded);
formdata.append('end', limit_reached)
$.ajax({
   url: "http://localhost:8000/faceTracker",
   type: "POST",
   data: formdata,
   processData: false,
   contentType: false,
}).done(function(respond){
  document.getElementById('overlay').src = "data:text/html;charset=utf-8," + escape(respond);
  postCanvasToURL();

}).fail(function(respond){
	
		postCanvasToURL();});

}

function submitCanvasToURL() {
	var d = new Date();
	var video = document.getElementById('videoElement');
  var canvas = document.getElementById('screenshot');
  canvas.getContext('2d').drawImage(video, 0, 0);
  // Convert canvas image to Base64
  var img = canvas.toDataURL();
  // Convert Base64 image to binary
  var file = dataURItoBlob(img);

  var formdata = new FormData();
formdata.append( 'avatar', file);
formdata.append('repeat', face_id + loaded);
formdata.append('end', false);
formdata.append('limit_reached', limit_reached);
if (d.getTime() < endtime) {
$.ajax({
   url: "http://localhost:8000/videosubmit",
   type: "POST",
   data: formdata,
   processData: false,
   contentType: false,
}).done(function(respond){
  document.getElementById('results_overlay').src = "data:text/html;charset=utf-8," + escape(respond);
  
  	
  submitCanvasToURL();
})
  } else {
    console.log("reached the end");
    formdata.set('end', true);
  	$.ajax({
   url: "http://localhost:8000/videosubmit",
   type: "POST",
   data: formdata,
   processData: false,
   contentType: false,
}).done(function(respond){
 console.log('response to end')

  	 document.getElementById('results_overlay').src = "data:text/html;charset=utf-8," + "<h1 style='color:white'>Time Limit Reached</h1>";
  	document.getElementById('overlay').src = "data:text/html;charset=utf-8,";
    callLimit();
  });
}

}

function dataURItoBlob(dataURI) {
// convert base64/URLEncoded data component to raw binary data held in a string
var byteString;
if (dataURI.split(',')[0].indexOf('base64') >= 0)
    byteString = atob(dataURI.split(',')[1]);
else
    byteString = unescape(dataURI.split(',')[1]);
// separate out the mime component
var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
// write the bytes of the string to a typed array
var ia = new Uint8Array(byteString.length);
for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
}
return new Blob([ia], {type:mimeString});
}

function callLimit() {
  $.ajax({
    async: 'false',
   url: "http://localhost:8000/videolimit",
   type: "POST",
}).done(function(respond){
  limit_reached = respond;
  console.log(respond)
});
}