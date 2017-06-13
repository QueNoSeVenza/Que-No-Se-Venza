var navsection = ["#navsection1", "#navsection2", "#navsection3"];

function hideSections() {
	$(navsection.join(', ')).hide();
}

function whiteNav() {
	$(".userText").css("color", "white");
	$(".menu-toggle .bars").removeClass("bars").addClass("barsTwo");
	$(".icon").css("background-color", "white");
	panel = false;
}

function greyNav() {
	$(".userText").css("color", "#616161");
	$(".menu-toggle .barsTwo").removeClass("barsTwo").addClass("bars");
	$(".icon").css("background-color", "#616161");
	panel = true;
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
	$('select').material_select();
	$('.collapsible').collapsible('open', 0);
	var toggle = $('.menu-toggle');

	// Fullpage
	$('#fullpage').fullpage({
		controlArrows: true,
		closeOnClick: true,
		loopHorizontal: false,
		keyboardScrolling: false,
		onSlideLeave: function (anchorLink, index, slideIndex, direction, nextSlideIndex) {
			var leavingSlide = $(this);
			if (slideIndex == 1) {
				whiteNav();
			}
			if (slideIndex == 2 || slideIndex == 0) {
				greyNav();
			}
		}
	});

	$('.button-collapse').sideNav({
		draggable: true // Choose whether you can drag to open on touch screens
	});

	$(toggle).click(function () {
		$(toggle).toggleClass('active');
		/*$('body').toggleClass('active');*/
	});

	$(".collapsible-header").click(function () {
		$(self).show();
	});

});