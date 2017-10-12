$(document).ready(function () {
    var grams = $("#donar_concentracion_gramos");
    var quantity = $("#donar_cantidad");

    $('#anio').change(function(event){
        checkDate();
    });

    $('#donar_concentracion_gramos').keyup(function(event){
        checkNumber(grams);
    });

    $('#donar_cantidad').keyup(function(event){
        checkNumber(quantity);
    });

    $('#sendDonar').click(function(event){
        checkSelects();
    });

    inicialiceCmbox();
});  

function inicialiceCmbox() {
    var currentDate = new Date();
    var currentYear = parseInt(currentDate.getFullYear());
    var listYears = [];
    var cmboxYear = $("#anio");
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
    var cmboxYear = $("#anio");
    var cmboxMonth = $("#mes");
    var currentDate = new Date();
    var currentYear = parseInt(currentDate.getFullYear());
    var currentMonth = parseInt(currentDate.getMonth());
    var selectYear = cmboxYear.val();
    if (selectYear == currentYear) {
        for (var i = 1; i < (currentMonth + 2); i++) {
            cmboxMonth.find("option[value='"+i+"']").prop("disabled",true);
        }
        $('#mes > option[value=""]').prop('selected', true)
        cmboxMonth.material_select();
    } else {
        for (var i = 1; i < (currentMonth + 2); i++) {
            cmboxMonth.find("option[value='"+i+"']").prop("disabled",false);
        }
        $('#mes > option[value=""]').prop('selected', true)
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
    
    selects.push($("#mes"));
    selects.push($("#anio"));
    selects.push($("#donar_tipo"));
    
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value == "") {
            console.log(inputs[i].value);
            return;
        }
    }
    for (var i = 0; i < selects.length; i++) {
        if (selects[i].val() == null) {
            return;
        }
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