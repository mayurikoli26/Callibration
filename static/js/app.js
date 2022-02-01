console.log("aap.js loaded");
// base.html required JS 
function myAction_vender(id) {
  document.getElementById("myForm").action = "/select_vender";
  document.getElementById("myForm").submit();
}
function myAction_dept() {
  document.getElementById("myForm").action = "/select_dept";
  document.getElementById("myForm").submit();
}
function myAction_logout() {
  document.getElementById("myForm").action = "/logout";
  document.getElementById("myForm").submit();
}
function myAction_post() {
  document.getElementById("myForm").action = "/postjason";
  document.getElementById("myForm").submit();
}


// parameter.html required JS functions

function show_no() {
  //document.getElementById("myForm").action = "/save_reading";
  var x = document.getElementById("myForm3").elements.length;
  var y = document.getElementById("myForm3").elements.item(4).value;
  var z = document.getElementById("myForm3").elements.namedItem("Remarks")
    .value;
  alert(x + y + z);
}
function getAllValues() {
  var x = document.getElementById("myForm3");
  // console.log(x);
  var txt = "";
  var i;
  for (i = 0; i < x.length; i++) {
    txt = txt + x.elements[i].value + "-";
    //txt = txt + x.elements[i].value.name+", ";
  }
  alert(txt);
  ////document.getElementById("myForm").element.namedItem("Remarks") = txt;
  //document.getElementById("textall").value = txt;
  //return txt;
}


function getAllValues1() {
    var x = document.getElementById("myForm3");
    var txt = "";
    var i;
    var txtname="";
    var jsontxt ="{";
    for (i = 0; i < x.length-1; i++) {
      txt = x.elements[i].value ;
      txtname = document.getElementById("myForm").elements[i].name;
      jsontxt = jsontxt + "\"" + txtname + "\"" + " : \"" + txt +"\",";
    }
    var jsonelem = jsontxt.replace(/,$/,'}');
    //document.getElementById("demo").innerHTML = patt1 ;
    alert (jsonelem) ;
  }

function onChecked(element) {
  var checkbox = document.getElementById(element);
  checkbox.value = checkbox.checked == true ? "1" : "0"
}

function getFormData(){ 
  var elements = document.getElementById("myForm3").elements;
  var obj ={};
  for(var i = 0 ; i < elements.length ; i++){
    var item = elements.item(i);
    obj[item.name] = item.value;
  }
  var formData = JSON.stringify(obj); //if you want string from json object  
  // document.getElementById("final_obj").value = formData;
  alert(formData)
  return formData;
}
function myAction_reading() {
  document.getElementById("myForm").reset();
}


