$(document).ready(function () {
    $('#meses').on("change", checkFecha);
    $('#anio').on("keyup", checkFecha);
    $('#n-gramos').on("keyup", checkGramos);
    $('#n-cantidad').on("keyup", checkCantidad);
    //$('#activa-fecha').on("mouseover", dissableButtonSend);
});    
    
function checkFecha() {
    var campoAnio = parseInt($("#anio").val());
    var campoMes = document.getElementById("meses");
    var corrienteFecha = new Date();
    var corrienteAnio = parseInt(corrienteFecha.getFullYear());
    var selectedMes = campoMes.options[campoMes.selectedIndex].value;
    
    if (isNaN(campoAnio) || campoAnio < corrienteAnio) {
        $("#anio").css("border-bottom-color","red");
        dissableButtonSend();
        return false;
    } else {
        $("#anio").css("border-bottom-color","grey");
        dissableButtonSend();
    }
    
    var timestampUsuario = new Date(campoAnio, selectedMes -1, 1).getTime();
    var timestampAhora = Date.now();
    
    if (timestampAhora > timestampUsuario) {
        console.log(timestampAhora +" ----> "+ timestampUsuario)
        $("#anio").css("border-bottom-color","red");
        document.getElementById("meses").style.borderBottomColor = "red";
        dissableButtonSend();
        return false;
    } else {
        $("#anio").css("border-bottom-color","grey");
        document.getElementById("meses").style.borderBottomColor = "grey";
        dissableButtonSend();
    }
}

function checkGramos() {
    var num1 = parseInt($("#n-gramos").val());
    
    if (num1 <= 0) {
        $("#n-gramos").css("border-bottom-color","red");
        $("#n-gramos").value = "red";
        dissableButtonSend();
        return false;
    } else {
        $("#n-gramos").css("border-bottom-color","grey");
        dissableButtonSend();
    }
}

function checkCantidad() {
    var num2 = parseInt($("#n-cantidad").val());
    
    if (num2 <= 0) {
        $("#n-cantidad").css("border-bottom-color","red");
        $("#n-cantidad").value = "red";
        dissableButtonSend();
        return false;
    } else {
        $("#n-cantidad").css("border-bottom-color","grey");
        dissableButtonSend();
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
    
    console.log(list_inputs)
    
    for (var i = 0; i < list_inputs.length; i++) {
        console.log(list_inputs[i])
        if (list_inputs[i] == "red") {
            console.log("red")
            $("#activa-fecha").prop("disabled", true);
            break;
        } else {
            console.log("grey")
            $("#activa-fecha").prop("disabled", false);
        }
    }
}