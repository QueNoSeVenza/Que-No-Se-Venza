$(document).ready(function () {
    // Revisa que los password sean iguales
    $("#regpass, #regpass2, #txtConfirmPassword").keyup(function (event) {
        checkPasswordMatch();
    });
    $("#terms").change(function (event) {
        dissableButtonSend();
    });

    // cambia form login o registrarse
    $(".register-content").hide();
    $("#regBtn").click(function() {
        $('.login-content').delay(360).hide(0);
        $(".login-card").animate({
            height: "40px"
        });
        $('.login-card').animate({
            height: "530px"
        });
        $('.register-content').delay(360).show(0);
    });
    $(".comingBack").click(function() {
        $('.register-content').delay(360).hide(0);
        $(".login-card").animate({
            height: "40px"
        });
        $('.login-card').animate({
            height: "420px"
        });
        $('.login-content').delay(360).show(0);
    });

    dissableButtonSend();
});

function checkPasswordMatch() {
    var password = $("#regpass").val();
    var confirmPassword = $("#regpass2").val();

    if (password != confirmPassword && confirmPassword!="" ){
        $("#regpass2").css("border-bottom-color","red");
        dissableButtonSend();
    } else if (password == confirmPassword && password != "" && confirmPassword != ""){
        $("#regpass2").css("border-bottom-color","green");
        dissableButtonSend();
    } else {
        $("#regpass2").css("border-bottom-color","grey");
        dissableButtonSend();
    }
}

function dissableButtonSend() {
    var inputs = $(".isRed");
    var terms = $("#terms");
    var list_inputs = [];
    for (var i = 0; i < inputs.length; ++i) {
        if (typeof inputs[i].attributes.id !== "undfined") {
            list_inputs.push(inputs[i].style.borderBottomColor);
        }
    }
    for (var i = 0; i < list_inputs.length; i++) {
        if (list_inputs[i] == "red" || terms.prop('checked')==false) {
            $("#register").prop("disabled", true);
            break;
        } else {
            $("#register").prop("disabled", false);
        }
    }
}

// esto hace que ande bien lo de los mesajes veeebozz
(function (exports) {
    function valOrFunction(val, ctx, args) {
        if (typeof val == "function") {
            return val.apply(ctx, args);
        } else {
            return val;
        }
    }

    function InvalidInputHelper(input, options) {
        input.setCustomValidity(valOrFunction(options.defaultText, window, [input]));

        function changeOrInput() {
            if (input.value == "") {
                input.setCustomValidity(valOrFunction(options.emptyText, window, [input]));
            } else {
                input.setCustomValidity("");
            }
        }

        function invalid() {
            if (input.value == "") {
                input.setCustomValidity(valOrFunction(options.emptyText, window, [input]));
            } else {
                input.setCustomValidity(valOrFunction(options.invalidText, window, [input]));
            }
        }

        input.addEventListener("change", changeOrInput);
        input.addEventListener("input", changeOrInput);
        input.addEventListener("invalid", invalid);
    }
    exports.InvalidInputHelper = InvalidInputHelper;
})(window);

InvalidInputHelper(document.getElementById("email"), {
    defaultText: "Ingrese una direccion de correo!",
    emptyText: "Ingrese una direccion de correo!",
    invalidText: function (input) {
        return 'La direccion de correo "' + input.value + '" no es valida!';
    }
});