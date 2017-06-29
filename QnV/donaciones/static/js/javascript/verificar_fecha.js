$(document).ready(function () {
/*    var corrienteDate = new Date();
    var corrienteMes = parseInt(corrienteDate.getMonth())+1;
    
    for(i=1; i<corrienteMes.length; i++) {
        var month = document.getElementById("meses").options[i].value;
        var mon = month-1;
        if(mon <= corrienteMes) {
            document.getElementById("meses").options[i].disabled = true;
        }
    }*/
    
    $('#meses').on("change", checkMes);
    $('#anio').on("keyup", checkAnio);
});    
    
function checkAnio() {
    var campoError = $("#mensajeError");
    var campoAnio = parseInt($("#anio").val());
    var campoMes = document.getElementById("meses");
    var corrienteFecha = new Date();
    var corrienteAnio = parseInt(corrienteFecha.getFullYear());
    var selectedMes = campoMes.options[campoMes.selectedIndex].value;
    
    if(isNaN(campoAnio) || campoAnio < corrienteAnio) {
        $("#anio").css("border-bottom-color","red");
        $("#activa-fecha").prop("disabled", true);
        campoError.text("ERROR EN AÑO");
        return false;
    } else {
        $("#anio").css("border-bottom-color","grey");
        $("#activa-fecha").prop("disabled", false);
    }
    
    var timestampUsuario = new Date(campoAnio, selectedMes -1, 1).getTime();
    var timestampAhora = Date.now();
    
    if(timestampAhora > timestampUsuario) {
        console.log(timestampAhora +" ----> "+ timestampUsuario)
        $("#anio").css("border-bottom-color","red");
        $("#activa-fecha").prop("disabled", true);
        campoError.text("ERROR FECHA VENCIDA");
        return false;
    } else {
        $("#anio").css("border-bottom-color","grey");
        $("#meses").css("border-bottom-color","grey");
        $("#activa-fecha").prop("disabled", false);
    }
}

function checkMes() {
    checkAnio();
}