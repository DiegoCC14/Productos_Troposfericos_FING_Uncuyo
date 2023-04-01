
function busqueda_productos_troposfericos(){
	
	console.log("Iniciar Busqueda !!!")
	

	var date_fecha_desde = new Date( $("#Fecha_desde").val() );
	var date_fecha_hasta = new Date( $("#Fecha_hasta").val() );
	if (date_fecha_desde <= date_fecha_hasta) {
	    console.log('Fechas Correcto');
	}else{
		mensaje_emergente( "Error: Campo Fecha" , "La fecha 'desde' es mayor o igual a fecha 'hasta' " )
		console.log('Fechas Incorrecto');
		return false //En caso de error terminamos proceso
	}
	

	if ( estaciones_para_busqueda.length == 0){
		mensaje_emergente( "Error: Campo Estaciones" , "No se ingresaron 'Estaciones' para la busqueda" )
		return false
	}


	let cabezera = []
	if ( $("#presion").is(":checked") || $("#temperatura").is(":checked") || $("#IWV").is(":checked") || $("#ZTD").is(":checked") ){
		
		if ( $("#presion").is(":checked") ){
			cabezera.push( 'presion' )
		}
		if ( $("#temperatura").is(":checked") ){
			cabezera.push( 'temperatura' )
		}
		if ( $("#IWV").is(":checked") ){
			cabezera.push( 'IWV' )
		}
		if ( $("#ZTD").is(":checked") ){
			cabezera.push( 'ZTD' )
		}
	}else{
		mensaje_emergente( "Error: Campo Cabezeras (presion,temperatura....)" , "Debe de seleccionar almenos una cabezera, temperatura, presion , IWZ , ZTD." )
		return false
	}

	//Verificamos si el Rango tiene datos

	let data_busqueda = {
		"fecha_desde": $("#Fecha_desde").val().replace("T"," "),
		"fecha_hasta": $("#Fecha_hasta").val().replace("T"," "),
		"headers": cabezera,
		"estaciones": estaciones_para_busqueda,
	}
	let texto_msj = "Cada 'Estacion' tarda entre 15s-1min de proceso"
	mensaje_emergente( "Envio Correcto: Se envio la consulta correctamente, " + estaciones_para_busqueda + ' Estaciones' ,  )
	

	console.log( { "data": JSON.stringify( data_busqueda ) } )	
	$.ajax({
        url: url_search_data_productos_troposfericos ,
        type:'get',
        data: { "data": JSON.stringify( data_busqueda ) } ,
        dataType:'JSON',
        success: function( request ){
            request["csvs_generados"].forEach( data_csv =>{
				window.open( "descarga_csv_user/" + data_csv["name"] + "/" );
            })
        },
        error: function( request ){
            console.log("Error Error Error")
        },
    })

}


function agregar_estacion_por_nombre(){

    let texto_estacion = $("#input_Estacion").val()
    estaciones_para_busqueda;
    estaciones_validas.forEach( dicc_estacion=>{
    	if( dicc_estacion["nombre"] == texto_estacion && !( estaciones_para_busqueda.includes( dicc_estacion["nombre"] ) )){
    		//Agregamos el elemento a la busqueda
    		let button_estacion = $("#button_estacion").clone().attr("display",true)
    		button_estacion.text(texto_estacion + " ")
    		button_estacion.addClass( "btn btn-primary" )
    		button_estacion.append( $( '<span class="badge bg-secondary" aria-hidden="true">&times;</span>' ) )
			$("#estaciones_de_busqueda").append( button_estacion )
			estaciones_para_busqueda.push( texto_estacion )
    		return true
    	}
    })
}


function agregar_estacion_por_rango_latitud_longitud(){
    estaciones_rango = []
    let latitud_norte = parseInt( $("#LatitudNorte").val() , 10 )
    let latitud_sur = parseInt( $("#LatitudSur").val() , 10 )
    let longitud_este = parseInt( $("#LongitudEste").val() , 10 )
    let longitud_oeste = parseInt( $("#LongitudOeste").val() , 10 )

    
    if ( !isNaN( latitud_norte ) && !isNaN( latitud_sur ) && !isNaN( longitud_este ) && !isNaN( longitud_oeste ) ){
    	estaciones_validas.forEach( dicc_estacion=>{ 
	    	if( dicc_estacion["longitud"]>=longitud_este && dicc_estacion["longitud"]<=longitud_oeste && dicc_estacion["latitud"]>=latitud_norte && dicc_estacion["latitud"]<=latitud_sur && !( estaciones_para_busqueda.includes( dicc_estacion["nombre"] ) ) ){
	    		//Agregamos el elemento a la busqueda
	    		let button_estacion = $("#button_estacion").clone().attr("display",true)
	    		button_estacion.text(dicc_estacion["nombre"] + " ")
	    		button_estacion.addClass( "btn btn-primary" )
	    		button_estacion.append( $( '<span class="badge bg-secondary" aria-hidden="true">&times;</span>' ) )
	    		$("#estaciones_de_busqueda").append( button_estacion )
	    		estaciones_para_busqueda.push( dicc_estacion["nombre"] )
	    		return true
	    	}
	    })
    }else{
    	if ( !isNaN( latitud_norte ) && !isNaN( latitud_sur ) ){

    		estaciones_validas.forEach( dicc_estacion=>{
		    	if( dicc_estacion["latitud"]>=latitud_norte && dicc_estacion["latitud"]<=latitud_sur && !( estaciones_para_busqueda.includes( dicc_estacion["nombre"] ) ) ){
		    		//Agregamos el elemento a la busqueda
		    		let button_estacion = $("#button_estacion").clone().attr("display",true)
		    		button_estacion.text(dicc_estacion["nombre"] + " ")
		    		button_estacion.addClass( "btn btn-primary" )
		    		button_estacion.append( $( '<span class="badge bg-secondary" aria-hidden="true">&times;</span>' ) )
		    		$("#estaciones_de_busqueda").append( button_estacion )
		    		estaciones_para_busqueda.push( dicc_estacion["nombre"] )
		    		return true
		    	}
		    })
	    }
	    if ( !isNaN( longitud_este ) && !isNaN( longitud_oeste ) ){
	    	estaciones_validas.forEach( dicc_estacion=>{ 
		    	if( dicc_estacion["longitud"]>=longitud_este && dicc_estacion["longitud"]<=longitud_oeste && !( estaciones_para_busqueda.includes( dicc_estacion["nombre"] ) ) ){
		    		//Agregamos el elemento a la busqueda
		    		let button_estacion = $("#button_estacion").clone().attr("display",true)
		    		button_estacion.text(dicc_estacion["nombre"] + " ")
		    		button_estacion.addClass( "btn btn-primary" )
		    		button_estacion.append( $( '<span class="badge bg-secondary" aria-hidden="true">&times;</span>' ) )
		    		$("#estaciones_de_busqueda").append( button_estacion )
		    		estaciones_para_busqueda.push( dicc_estacion["nombre"] )
		    		return true
		    	}
		    })
	    }
	    console.log("Numero no valido")
    } 
}


function mensaje_emergente( titulo , mensaje ){
	$("#popup").find("#titulo_mensaje").text( titulo )
	$("#popup").find("#texto_mensaje").text( mensaje )
	mostrarPopup()
}

function mostrarPopup() {
	var popup = document.getElementById("popup");
	popup.style.display = "flex";
}

function cerrarPopup() {
	var popup = document.getElementById("popup");
	popup.style.display = "none";
}



function obteniendo_y_ingresando_estaciones_validas(){
	
	$.ajax({
        url: url_estaciones_disponibles ,
        type:'get',
        data: {} ,
        dataType:'JSON',
        success: function( request ){
			console.log( request["Estaciones"] )
			estaciones_validas = request["Estaciones"]
			request["Estaciones"].forEach( estacionObj => {
				$("#estaciones_list_data").append($("<option>").attr('value',estacionObj["nombre"]).text(estacionObj["nombre"]));
			} )
        },
        error: function( request ){
            console.log("Error Error Error")
            reject(error);
        },
    })

}



var hidden_div_estacion = true
var hidden_div_rango_estacion = true
var estaciones_para_busqueda = [];


$(document).ready(function () {
	
	console.log("Documento Cargado")
	
	var estaciones_validas; //Array global que contiene las estaciones Validas 
	var estaciones_para_busqueda = []; //Array global que contiene las estaciones que seran buscadas
	
	obteniendo_y_ingresando_estaciones_validas() //Obtenemos l

} )
