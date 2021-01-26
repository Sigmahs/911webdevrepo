var crime_color = "#302f2f";
var crime_alert_color = "#737373";
var emergency_color = "#cf0101";
var medical_color = "#4a69d4";
var medical_alert_color = "#42a8fa";
var no_action_color = "#8bd8aa";
var no_emergency_color= "#0bcc58";

function image_hover(element) {
  var rect = element.getBoundingClientRect();
  var type1 = element.className.split(' ')[1];
  setBar(type1, "top");
  var type2 = element.className.split(' ')[2];
  setBar(type2, "bottom");

  var boxElement = document.getElementById("info-box");
  var lineElement = document.getElementById("info-line");
  var dotElement = document.getElementById("info-dot");
  boxElement.style.display = "block";
  lineElement.style.display = "block";
  dotElement.style.display = "block";

  if (rect.right > screen.width / 2) {
    boxElement.style.left = rect.left - rect.width * 2.25 + "px";
    lineElement.style.left = rect.left - rect.width * 0.2 + "px";
    dotElement.style.left = rect.left + rect.width * 0.1 + "px";
  } else {
    boxElement.style.left = rect.right - rect.width * 0.12 + "px";
    lineElement.style.left = rect.right - rect.width * 0.18 + "px";
    dotElement.style.left = rect.right - rect.width * 0.18 + "px";
  }
  boxElement.style.top = rect.top - rect.height / 3 + "px";
  lineElement.style.top = rect.top + rect.height * 0.45 + "px";
  dotElement.style.top = rect.top + rect.height * 0.45 + "px";


}

function setBar(type, bar) {
  var bar;
  var typeText;
  if (bar == "top") {
    bar = document.getElementById("top-colored");
    typeText = document.getElementById("top-text");
  } else {
    bar = document.getElementById("bottom-colored");
    typeText = document.getElementById("bottom-text");
  }

  switch (type) {
    case "crime":
      bar.style.backgroundColor = crime_color;
      typeText.innerHTML = "Crime";
      break;
    case "crime-alert":
      bar.style.backgroundColor = crime_alert_color;
      typeText.innerHTML = "Crime Alert";
      break;
    case "emergency":
      bar.style.backgroundColor = emergency_color;
      typeText.innerHTML = "Emergency";
      break;
    case "medical":
      bar.style.backgroundColor = medical_color;
      typeText.innerHTML = "Medical";
      break;
    case "medical-alert":
      bar.style.backgroundColor = medical_alert_color;
      typeText.innerHTML = "Medical Alert";
      break;
    case "no-action":
      bar.style.backgroundColor = no_action_color;
      typeText.innerHTML = "No Action";
      break;
    case "no-emergency":
      bar.style.backgroundColor = no_emergency_color;
      typeText.innerHTML = "No Emergency";
      break;
  }
}

function image_off(element) {
  var boxElement = document.getElementById("info-box");
  var lineElement = document.getElementById("info-line");
  var dotElement = document.getElementById("info-dot");
  boxElement.style.display = "none";
  lineElement.style.display = "none";
  dotElement.style.display = "none";
}



//size too big error message
function testSize(input) {
  if (input.files[0].size >= 2*1024*1024) {
    alert('Image size too large. Please try again.');
  } else {
    readURL(input);
    wheelLoader();
  }
}

function readURL(input) {
  this.thing = input;
  document.getElementById("number").value = face_id + loaded;
  if (input.files && input.files[0]) {
    url = document.getElementById("url").innerHTML;



    var reader = new FileReader();
    reader.onload = function (e) {
      $('#image-preview').attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
  $("#myform").submit();
}

//Plotly Pie Chart with grouping of any values after the largest three
/*var data = [{
values: [0.96, 12.68, 3, 0.04, 82.56, 0.2, 0.07, 0.48],
labels: ['Disgust', 'Contempt','Anger' , 'Fear',
'Happiness', 'Neutrality', 'Sadness', 'Surprise'],
type: 'pie'
}];
var no_values = data[0].values.length;
if (no_values > 4) {
var arr = data[0].values.slice(0);
var list = [];
for (var j = 0; j < no_values - 3; j++) {
list.push(index_of_min(arr));
arr[index_of_min(arr)] = 100;
}
data[0].labels.push('Other');
data[0].values.push(0);
list.sort();
for (var j = 0; j < list.length; j++) {
data[0].values[8-j] += data[0].values[list[j]-j];
data[0].values.splice(list[j]-j, 1);
data[0].labels.splice(list[j]-j, 1);
}
}*/

function index_of_min(arr) {
  var min = arr[0];
  var minindex = 0;
  for (var i = 1; i < arr.length; i++) {
    if (arr[i] <= min) {
      minindex = i;
      min = arr[i];
    }
  }
  return minindex;
}

var loaded = 0
var face_id = 0
window.onload=function () {
  face_id = '_' + Math.random().toString(36).substr(2, 9);
};

function boxer() {

  /*if (loaded < 0) {
  url = document.getElementById("url").innerHTML;
  $('#image-preview').attr('src', url);
  new_url = url.split("_");
  console.log(new_url);
  new_number = (parseInt(new_url[new_url.length - 1].split(".")[0]) + 1).toString()+"." + new_url[new_url.length - 1].split(".")[1];
  console.log(new_number);
  new_url[new_url.length - 1] = new_number;
  new_url = new_url.join("_");
  document.getElementById("url").innerHTML = new_url;
  console.log(new_url);

}*/
loaded += 1;
document.getElementById("number").value = face_id + loaded;
}


function upload() {
  var uploadField = document.getElementById("file");
  uploadField.onchange = function() {
    if(this.files[0].size > 2097152){
      alert("File size must be under 2MB.");
      this.value = "";
    };
    testSize(this)
  };
  uploadField.click();

};

function wheelLoader() {
  document.getElementById("image-loading").style.visibility = "visible";
}

function wheelLoaderHider() {
  document.getElementById("image-loading").style.visibility = "hidden";
}
