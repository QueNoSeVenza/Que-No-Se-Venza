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
	firstSection();
	// Materialize
	$('select').material_select();
	$('.collapsible').collapsible('open', 0);
	$('.datepicker').pickadate({
		selectMonths: true, // Creates a dropdown to control month
		selectYears: 15 // Creates a dropdown of 15 years to control year
	});
	var toggle = $('.menu-toggle');

	// Fullpage
	$('#fullpage').fullpage({
		controlArrows: true,
		closeOnClick: true,
		loopHorizontal: false,
		keyboardScrolling: false,
		scrollOverflow: true,
		/*		onSlideLeave: function (anchorLink, index, slideIndex, direction, nextSlideIndex) {
					var leavingSlide = $(this);
					if (slideIndex == 1) {
						whiteNav();
					}
					if (slideIndex == 2 || slideIndex == 0) {
						greyNav();
					}
				}*/
	});


	$('.button-collapse').sideNav({
		draggable: true // Choose whether you can drag to open on touch screens
	});

	$(toggle).click(function () {
		$(toggle).toggleClass('active');
		if ($('.menu-toggle span').hasClass('bars')) {
			$(".menu-toggle .bars").removeClass("bars").addClass("barsTwo");
		} else {
			$(".menu-toggle .barsTwo").removeClass("barsTwo").addClass("bars");
		}
		/*$('body').toggleClass('active');*/
	});

	$(".collapsible-header").click(function () {
		$(self).show();
	});

});