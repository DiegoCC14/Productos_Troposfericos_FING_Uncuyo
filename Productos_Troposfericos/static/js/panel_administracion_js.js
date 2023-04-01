function actualizar_LatLongAlt(){
	console.log("Variable Funcionando")

    var data = new FormData();
    console.log( $( '#csvEstacionesLatLongAlt' )[0].files[0] )
    data.append( 'CSV_EST_LAT_LONG_ALT' , $('#csvEstacionesLatLongAlt')[0].files[0] );

    $.ajax({
    	headers: {'X-CSRFToken': CSRF_TOKEN} ,
        url: url_actualizar_lat_long_alt_estaciones_datos_troposfericos ,
        data: data,
        processData: false,
  		contentType: false,
        type: 'POST',
        success: function ( request ) {
       		console.log( request )
        },
        error: function( request ){
            console.log("Error Error Error")
        },
    });

}

$(document).ready(function () {
	console.log("Documento Cargado")
} )
