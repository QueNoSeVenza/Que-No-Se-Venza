var panel = true;
		var navsection = ["#navsection1", "#navsection2", "#navsection3"];

		function hideSections() {
			$(navsection.join(', ')).hide();
		}

		function toLeft() {
			$.fn.fullpage.moveSlideLeft();
			if (panel) {
				$(".userText").css("color", "white");
				$(".menu-toggle .bars").removeClass("bars").addClass("barsTwo");
				$(".icon").css("background-color", "white");
				panel = false;
			} else {
				$(".userText").css("color", "#616161");
				$(".menu-toggle .barsTwo").removeClass("barsTwo").addClass("bars");
				$(".icon").css("background-color", "#616161");
				panel = true;
			}
		}

		function toRight() {
			$.fn.fullpage.moveSlideRight();
			if (panel) {
				$(".userText").css("color", "white");
				$(".menu-toggle .bars").removeClass("bars").addClass("barsTwo");
				$(".icon").css("background-color", "#fff");
				panel = false;
			} else {
				$(".userText").css("color", "#616161");
				$(".menu-toggle .barsTwo").removeClass("barsTwo").addClass("bars");
				$(".icon").css("background-color", "#616161");
				panel = true;
			}
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

		$(document).ready(function() {
			firstSection();

			$('.collapsible').collapsible('open', 0);
			var toggle = $('.menu-toggle');

			$('#wrapper').fullpage({
				controlArrows: false,
				closeOnClick: true,
			});

			$('.button-collapse').sideNav({
				draggable: true // Choose whether you can drag to open on touch screens
			});

			$(toggle).click(function() {
				$(toggle).toggleClass('active');
				/*$('body').toggleClass('active');*/
			});

			$(".collapsible-header").click(function() {
				$(self).show();
			});

			$("#applybtn").click(function() {

			});
		});
