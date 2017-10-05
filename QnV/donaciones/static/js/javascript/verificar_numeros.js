$(document).ready(function () {
    var grams = $("#n-gramos");
    var quantity = $("#n-cantidad");

    $('#anios').change(function(event){
        checkDate();
    });

    $('#n-gramos').keyup(function(event){
        checkNumber(grams);
    });

    $('#n-cantidad').keyup(function(event){
        console.log("ne");
        checkNumber(quantity);
    });

    $('#sendDonar').click(function(event){
        console.log("pe");
        checkSelects();
    });

    inicialiceCmbox();
});  

function inicialiceCmbox() {
    var currentDate = new Date();
    var currentYear = parseInt(currentDate.getFullYear());
    var listYears = [];
    var cmboxYear = $("#anios");
    for (var i = 0; i < 15; i++) {
        listYears.push(currentYear + i);
    }
    for (var i = 0; i < listYears.length; i++) {
        $option = $('<option>', 
                    { 
            value : listYears[i],
            text : listYears[i]
        }
                   );
        cmboxYear.append($option);
    }
    cmboxYear.material_select();
}

function checkDate() {
    var cmboxYear = $("#anios");
    var cmboxMonth = $("#meses");
    var currentDate = new Date();
    var currentYear = parseInt(currentDate.getFullYear());
    var currentMonth = parseInt(currentDate.getMonth());
    var selectYear = cmboxYear.val();
    if (selectYear == currentYear) {
        for (var i = 1; i < (currentMonth + 2); i++) {
            cmboxMonth.find("option[value='"+i+"']").prop("disabled",true);
        }
        $('#meses > option[value=""]').prop('selected', true)
        cmboxMonth.material_select();
    } else {
        for (var i = 1; i < (currentMonth + 2); i++) {
            cmboxMonth.find("option[value='"+i+"']").prop("disabled",false);
        }
        $('#meses > option[value=""]').prop('selected', true)
        cmboxMonth.material_select();
    }
}

function checkNumber(sel) {
    var selectNumber = parseInt(sel.val());
    console.log(selectNumber);
    console.log(sel);
    console.log("gas");
    if (selectNumber <= 0) {
        sel.css("border-bottom-color","red");
        dissableButtonSend();
        return false;
    } else {
        sel.css("border-bottom-color","grey");
        dissableButtonSend();
    }
}

function checkSelects() {
    var inputs = document.getElementsByClassName("isInput");
    var selects = [];
    var inputsValue = [];
    var salida;
    
    selects.push($("#meses"));
    selects.push($("#anios"));
    selects.push($("#tipo"));
    
    console.log(selects);
    console.log(inputs);
    
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value == "") {
            console.log(inputs[i].value);
            salida = "no";
            return;
        } else {
            salida = "si";
            console.log(inputs[i].value);
            console.log(salida);
        }
    }
    for (var i = 0; i < selects.length; i++) {
        if (selects[i].val() == null) {
            return;
        }
    }
    if (salida == "si") {
        console.log("estoy en salida");
        for (var i = 0; i < inputs.length; i++) {
            inputsValue.push(inputs[i].value);
        }
        $("#n_1").val(inputsValue[0]);
        $("#c_1").val(inputsValue[1]);
        $("#ca_2").val(inputsValue[2]);
        $("#l_1").val(inputsValue[3]);
        $("#d_1").val(inputsValue[4]);
        $("#f_1").val(selects[1].val());
        $("#f_2").val(selects[0].val());
        $("#t_1").val(selects[2].val());
        $("#ahref")[0].click();
    }
}

function dissableButtonSend() {
    var inputs = document.getElementsByClassName("isInput");
    var list_inputs = [];
    for (var i = 0; i < inputs.length; ++i) {
        if (typeof inputs[i].attributes.id !== "undfined") {
            list_inputs.push(inputs[i].style.borderBottomColor);
        }
    }
    for (var i = 0; i < inputs.length; i++) {
        if (list_inputs[i] == "red" || inputs[i].val == "") {
            $("#sendDonar").prop("disabled", true);
            break;
        } else {
            $("#sendDonar").prop("disabled", false);
        }
    }
}