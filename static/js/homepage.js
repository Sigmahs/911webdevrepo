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