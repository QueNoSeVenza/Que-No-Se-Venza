var navsection = ["#navsection1", "#navsection2", "#navsection3"];

function hideSections() {
	$(navsection.join(', ')).hide();
}


function toLeft() {
	$.fn.fullpage.moveSlideLeft();
}

function toRight() {
	$.fn.fullpage.moveSlideRight();
}

function firstSection() {
	hideSections();
	$('#navsection1').fadeIn("100");
};

function secondSection() {
	hideSections();
	$('#navsection2').fadeIn("100");
};

function thirdSection() {
	hideSections();
	$('#navsection3').fadeIn("100");
};

$(document).ready(function () {
	$(".extra_info").hide()
    $("#pedir_nombre,#pedir_gramos").change(function () {
    	var nombre = $("#pedir_nombre").val();
    	var concentracion = $("#pedir_gramos").val();
    	if (nombre != "" && concentracion != ""){
      $.ajax({
        url: '/ajax/validate_medicamento/',
        data: {
          'nombre': nombre,
          'concentracion' : concentracion
        },
        dataType: 'json',
        success: function (data) {
          if (!data.exists) {
          	$(".extra_info").show()
            alert("Este medicamento todavia no se encuentra en nuestra base de datos, por favor, completa los demás campos para que podamos avisarte si alguien lo dona en el futuro");
          }else{$(".extra_info").hide()}
        }
      })};

    });



	var sidenav = $('.side-nav');
	firstSection();
	// Materialize
	$('select').material_select();
	$('.collapsible').collapsible('open', 0);
	$('.datepicker').pickadate({
		selectYears: 15 // Creates a dropdown of 15 years to control year
		// format: 'YYYY-MM-DD'
	});
	$('.button-collapse').sideNav({
		draggable: true // Choose whether you can drag to open on touch screens
	});
	$(".collapsible-header").click(function () {
		$(self).show();
	});

	// Fullpage
	$('#fullpage').fullpage({
		controlArrows: true,
		closeOnClick: true,
		loopHorizontal: false,
		keyboardScrolling: false,
		scrollOverflow: true,
		responsiveHeight: 900,
	});
	var toggle = $('.menu-toggle');
	$(toggle).click(function () {
		document.getElementById('sidenav').style.pointerEvents = 'none';
		sidenav.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
			function (e) {
				document.getElementById('sidenav').style.pointerEvents = 'auto';
				if ($('.menu-toggle').hasClass('active')) {
					/*Cambiar a blanco*/
					$(".menu-toggle .barsTwo").removeClass("barsTwo").addClass("bars");
					$(toggle).toggleClass('active');
					console.log(toggle);
				} else {
					/*Cambiar a gris*/
					$(".menu-toggle .bars").removeClass("bars").addClass("barsTwo");
					$(toggle).toggleClass('active');
					console.log(toggle);
				}
			});
	});
	/*$('body').toggleClass('active');*/


});
