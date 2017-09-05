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
        checkNumber(quantity);
    });
    
    $('#sendDonar').click(function(event){
        console.log("pene");
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
        $('#meses > option[value="0"]').prop('selected', true)
        cmboxMonth.material_select();
    } else {
        for (var i = 1; i < (currentMonth + 2); i++) {
            cmboxMonth.find("option[value='"+i+"']").prop("disabled",false);
        }
        $('#meses > option[value="0"]').prop('selected', true)
        cmboxMonth.material_select();
    }
}

function checkNumber(sel) {
    var selectNumber = parseInt(sel.val());
    console.log(selectNumber);
    console.log(sel);
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
    var validateSelectMonth = $("#anios");
    var validateSelectYear = $("#meses");
    console.log(validateSelectMonth.val() + "  , " + validateSelectYear.val());
    if (validateSelectMonth.val() == ""){
        /*validateSelectMonth.css("border-bottom-color","red");
        validateSelectMonth.material_select();*/
        return false;
    } else if (validateSelectYear.val() == ""){
        /*validateSelectYear.css("border-bottom-color","red");
        validateSelectYear.material_select();*/
        return false;
    }
}

function dissableButtonSend() {
    var inputs = document.getElementsByClassName("isRed");
    var list_inputs = [];
    for (var i = 0; i < inputs.length; ++i) {
        if (typeof inputs[i].attributes.id !== "undfined") {
            list_inputs.push(inputs[i].style.borderBottomColor);
        }
    }
    for (var i = 0; i < list_inputs.length; i++) {
        if (list_inputs[i] == "red") {
            $("#sendDonar").prop("disabled", true);
            break;
        } else {
            $("#sendDonar").prop("disabled", false);
        }
    }
}