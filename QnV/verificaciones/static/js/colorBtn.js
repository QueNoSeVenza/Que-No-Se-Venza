$(document).ready(function () {
	btnColor();	
	$(".Inactivo").hide()
	$(".btn-delete").click(function(){
	var itemid = $(this).attr('value')
	if(confirm('¿Estas seguro de que deseas eliminar este medicamento?')){
	$.ajax({
		url: '/ajax/delete_stock/',
		data: {
			'itemid': itemid,
			},
			dataType: 'json',
			success: function (data) {
			
				$("#"+itemid).hide()
			}
		})}

}); 
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