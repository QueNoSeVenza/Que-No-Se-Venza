$(document).ready(function () {
	btnColor();	
});  


function btnColor() {
	var pathname = window.location.pathname;
	console.log(pathname);
	switch (pathname) {
		case '/verificacion/stock':
			$('#stock').addClass('button-primary');
			$('#entrada').removeClass('button-primary');
			$('#retiro').removeClass('button-primary');
			break;
		case '/verificacion/input/entrada/':
			$('#entrada').addClass('button-primary');
			$('#stock').removeClass('button-primary');
			$('#retiro').removeClass('button-primary');
			break;
		case '/verificacion/input/retiro/':
			$('#retiro').addClass('button-primary');
			$('#stock').removeClass('button-primary');
			$('#entrada').removeClass('button-primary');
	}
		
}