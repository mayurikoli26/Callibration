// previous_reading_n

function getAllValues2() {
    var y = document.getElementById("myForm");
    console.log(y)
    var txt = "";
    var i;
    var txtname = "";
    var jsontxt = "{";

    var fruits, text, fLen, i, n, index_flag = "False",
        txtn = "";
    for (j = 0; j < y.length; j++) {
        if (index_flag == "True") {
            index_flag = "False";
            continue;
        }
        text = y.elements[j].value;

        continue;

    }
    x = y;
    for (i = 0; i < x.length - 10; i++) {
        txt = x.elements[i].value;
        //alert("No1");
        txtname = document.getElementById("myForm").elements[i].name;
        //alert("No2 ");
        jsontxt = jsontxt + "\"" + txtname + "\"" + " : \"" + txt + "\",";
    }
    var jsonelem = jsontxt.replace(/,$/, '}');
    //document.getElementById("demo").innerHTML = patt1 ;

    document.getElementById("textall").value = jsonelem;
    return (jsonelem)
}

// parameter_input_input 
function getAllValues2() {
    var y = document.getElementById("myForm");
    console.log(y)
    var txt = "";
    var i;
    var txtname = "";
    var jsontxt = "{";

    var fruits, text, fLen, i, n, index_flag = "False",
        txtn = "";
    for (j = 0; j < y.length; j++) {
        if (index_flag == "True") {
            index_flag = "False";
            continue;
        }
        text = y.elements[j].value;

    }
    x = y;
    for (i = 0; i < x.length - 10; i++) {
        txt = x.elements[i].value;

        txtname = document.getElementById("myForm").elements[i].name;

        jsontxt = jsontxt + "\"" + txtname + "\"" + " : \"" + txt + "\",";
    }
    var jsonelem = jsontxt.replace(/,$/, '}');


}

// add_equipment 

function getAllValues3() {
    var y = document.getElementById("myForm4");
    console.log()
    var txt = "";
    var i;
    var txtname = "";
    var jsontxt = "{";

    var fruits, text, fLen, i, n, index_flag = "False",
        txtn = "";
    for (j = 0; j < y.length; j++) {
        if (index_flag == "True") {
            index_flag = "False";
            continue;
        }
        text = y.elements[j].value;

        continue;

    }
    x = y;
    for (i = 0; i < x.length - 10; i++) {
        txt = x.elements[i].value;
        //alert("No1");
        txtname = document.getElementById("myForm4").elements[i].name;
        //alert("No2 ");
        jsontxt = jsontxt + "\"" + txtname + "\"" + " : \"" + txt + "\",";
    }
    var jsonelem = jsontxt.replace(/,$/, '}');
    //document.getElementById("demo").innerHTML = patt1 ;
    console.log(jsonelem)
    alert(jsonelem);
    document.getElementById("textall").value = jsonelem;

    return (jsonelem)

}