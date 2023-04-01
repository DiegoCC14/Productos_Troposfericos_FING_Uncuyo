
function busqueda_productos_troposfericos(){
	console.log("Iniciar Busqueda !!!")
	
	var date_fecha_desde = new Date( $("#Fecha_desde").val() );
	var date_fecha_hasta = new Date( $("#Fecha_hasta").val() );
 	
	if (date_fecha_desde <= date_fecha_hasta) {
	    console.log('Fechas Correcto');
	}else{
		console.log('Fechas Incorrecto');
		return false //En caso de error terminamos proceso
	}
	
	let busqueda_estacion = estacines_validas.find( estacion_json => estacion_json["nombre"] == $("#input_Estacion").val() );
	if ( busqueda_estacion != undefined ) {
	    console.log('Esctacion Valida ' +  $("#input_Estacion").val());
	}else{	
		console.log('Estacion No Valida ' + $("#input_Estacion").val() );
		//Realizamos peticion Estaciones
		estacines_validas = obteniendo_estaciones_validas()
		return false //En caso de error terminamos proceso
	}
	
	let cabezera = []

	if ( $("#presion").is(":checked") || $("#temperatura").is(":checked") || $("#IWV").is(":checked") || $("#ZTD").is(":checked") ){
		
		if ( $("#temperatura").is(":checked") ){
			cabezera.push( 'temperatura' )
		}
		if ( $("#presion").is(":checked") ){
			cabezera.push( 'presion' )
		}
		if ( $("#IWV").is(":checked") ){
			cabezera.push( 'IWV' )
		}
		if ( $("#ZTD").is(":checked") ){
			cabezera.push( 'ZTD' )
		}
	}else{
		console.log("Ninguna Cabezera seleccionada presion || temperatura || IWV || ZTD")
		return false
	}

	let data_busqueda = {
		"fecha_desde": $("#Fecha_desde").val().replace("T"," "),
		"fecha_hasta": $("#Fecha_hasta").val().replace("T"," "),
		"headers": cabezera,
		"estacion": $("#input_Estacion").val(),
	}

	console.log("Data a Enviar 123123" )
	console.log( { "data": JSON.stringify( data_busqueda ) } )
	
	$.ajax({
        url: url_search_data_productos_troposfericos ,
        type:'get',
        data: { "data": JSON.stringify( data_busqueda ) } ,
        dataType:'JSON',
        success: function( request ){
            console.log( request )
        },
        error: function( request ){
            console.log("Error Error Error")
        },
    })

}

function obteniendo_estaciones_validas(){
	let estaciones_validas_list = [
		{ "id":1  , "nombre":'MSFW' },
		{ "id":2  , "nombre":'DSAD' },
		{ "id":3  , "nombre":'FFWF' },
		{ "id":4  , "nombre":'FSDA' },
		{ "id":5  , "nombre":'GRES' },
		{ "id":6  , "nombre":'FDWW' },
		{ "id":7  , "nombre":'VVDD' },
		{ "id":8  , "nombre":'GHGT' }
	]
	/*
	Peticiones POST
	*/
	return estaciones_validas_list
}

var hidden_div_estacion = true
var hidden_div_rango_estacion = true
var estacines_validas = []

$(document).ready(function () {
	console.log("Documento Cargado")
	
	$("#Estacionbutton").click(function () {
		console.log( hidden_div_estacion )
		if (hidden_div_estacion==true){
			$("#div_estaciones").attr("hidden",false);
			hidden_div_estacion = false
		}else{
			$("#div_estaciones").attr("hidden",true);
			hidden_div_estacion = true
		}
	});

	$("#Rangobutton").click(function () {
		console.log( hidden_div_rango_estacion )
		if (hidden_div_rango_estacion==true){
			$("#div_estaciones_rango").attr("hidden",false);
			hidden_div_rango_estacion = false
		}else{
			$("#div_estaciones_rango").attr("hidden",true);
			hidden_div_rango_estacion = true
		}
	});

	estacines_validas = obteniendo_estaciones_validas()
	estacines_validas.forEach( estacion_json => {
		$("#estaciones_list_data").append($("<option>").attr('value', estacion_json["id"] ).text( estacion_json["nombre"] ));
	} )

} )
