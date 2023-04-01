from .Generador_de_JSON_service import retorna_ultima_actividad_generada , Generador_de_JSON_Actividades_Mendoza

from bs4 import BeautifulSoup
import requests , pathlib , parse


DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual


def get_data_actualizada_productos_troposfericos():
	url_Productos_Troposfericos = f"https://cima.ingenieria.uncuyo.edu.ar/IWV_ERA5/productos"
	page = requests.get( url_Productos_Troposfericos )
	soup = BeautifulSoup( page.content , "html.parser" )

	id_list_noticias = soup.find_all( "pre" ) 
	lista_pre = id_list_noticias[0].text.replace("../","").split(" -") #Dividimos por " -"

	Lista_anios_data = []
	for data_anio in [ list_texto.split() for list_texto in lista_pre[0:len(lista_pre)] if len(list_texto.split())>0 ]:
		if len( data_anio ) == 3:
			data_anio = { 'nombre':data_anio[0] ,
							'csv':[] ,
							'fecha_modificasion':data_anio[1] ,
							'hora_modificasion':data_anio[2] ,
							"link":f"{url_Productos_Troposfericos}/{data_anio[0]}",
							"Estado" : "Desconocido"}
			
			page_anio = requests.get( data_anio["link"] )
			soup_anio = BeautifulSoup( page_anio.content , "html.parser" )

			csvs_anio = soup_anio.find_all( "pre" )[0].text.replace("../","").split("\r\n")

			for list_csv_anio in [ texto_csv.split() for texto_csv in csvs_anio if len(texto_csv.split())>0 ]:
				if len(list_csv_anio)==4: #La lista solo tiene que tener 3 elementos
					data_dict = {
						'nombre': list_csv_anio[0],
						'link': f"{data_anio['link']}{list_csv_anio[0]}",
						'fecha_modificasion': list_csv_anio[1],
						'hora_modificasion': list_csv_anio[2],
						'peso_kbits': list_csv_anio[3].replace("K",""),
						"Estado": "Desconocido"}
					
					data_anio["csv"].append( data_dict )
					
				else:
					print( f"Error Scrapign CSV {list_csv_anio}" )
					return {"Datos":[] , "Mensaje":f"Error Scrapign CSV {list_csv_anio}"}
		
			Lista_anios_data.append(data_anio)

		else:
			print(f"Error Scraping Anio {data_anio}")
			return {"Datos":[] , "Mensaje":f"Error Scraping Anio {data_anio}"}

	return {"Datos": Lista_anios_data , "Mensaje":"Correcto" } 


def Conversor_de_fechas_mes_dia_anio( fecha , List_Formatos_Fechas_Compilados ):
	
	Meses = {'enero':1 ,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,
		'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12,
		'ene':1 ,'feb':2 ,'mar':3 ,'abr':4 ,'may':5 ,'jun':6 ,'jul':7 ,'ago':8 ,'sep':9 ,
		'oct':10 ,'nov':11 ,'dic':12 ,
		'jan':1 ,'feb':2 ,'mar':3 ,'apr':4 ,'may':5 ,'jun':6 ,'jul':7 ,'aug':8 ,'sep':9 , #Ingles
 		'oct':10 ,'nov':11 ,'dec':12 }
	
	for Formato_ER in List_Formatos_Fechas_Compilados:
		resultado_fecha = Formato_ER.parse( fecha )
		
		if resultado_fecha != None:
			dia = resultado_fecha["num_dia"]
			mes = Meses[ resultado_fecha["mes"].lower() ]
			anio = resultado_fecha["anio"]

			fecha_resultado = f'{anio}-{mes}-{dia}' #YYYY-MM-DD , valido DB

			return fecha_resultado
	
	return fecha #Devolvemos la misma fecha

def tratamiento_datos_data_productos_troposfericos( list_productos_troposfericos ):
	
	#ETC , extraccion , TRANSFORMACION , Carga de Datos
	
	formato_fecha_1 = parse.compile('{mes:S} {num_dia:d}, {anio:d}' ) # 'junio 27, 2022' , 'Junio 16, 2022'
	formato_fecha_2 = parse.compile( '{num_dia:d} {mes:S}, {anio:d}' ) # '28 junio, 2022'
	formato_fecha_3 = parse.compile( '{num_dia:d} {mes:S} {anio:d}' ) # '28 Ago 2022'
	formato_fecha_4 = parse.compile( '{num_dia:d} de {mes:S}, {anio:d}' ) # '28 Ago 2022'
	formato_fecha_5 = parse.compile( '{num_dia:d}-{mes:S}-{anio:d}' ) # "29-Apr-2022"
	List_Formatos_Fechas_Compilados = [ formato_fecha_1 , formato_fecha_2 , formato_fecha_3 , formato_fecha_4 , formato_fecha_5 ]

	for data_year in list_productos_troposfericos:
		data_year["fecha_modificasion"] = Conversor_de_fechas_mes_dia_anio( data_year["fecha_modificasion"] , List_Formatos_Fechas_Compilados )
		for data_csv in data_year["csv"]:
			data_csv['fecha_modificasion'] = Conversor_de_fechas_mes_dia_anio( data_csv['fecha_modificasion'] , List_Formatos_Fechas_Compilados )

	return list_productos_troposfericos

def comparacion_data_actual_con_data_anterior( list_data_anterior , list_data_actual ):
	#Retornoa una data_actual con Estados actualizados, y un booleano por si es necesario generar nuevo json historico
	
	Existen_Cambios = False

	#Buscando diferencias entre anio actual y anterior
	for anio_data_actual in list_data_actual:
		
		New_Data_Anio = True
		
		for anio_data_anterior in list_data_anterior:
			
			if anio_data_anterior["nombre"] == anio_data_actual["nombre"]:
				
				fecha_mod_anio_actual = anio_data_actual["fecha_modificasion"] + anio_data_actual["hora_modificasion"]
				fecha_mod_anio_anterior = anio_data_anterior["fecha_modificasion"] + anio_data_anterior["hora_modificasion"] 
				
				if fecha_mod_anio_actual==fecha_mod_anio_anterior:
					anio_data_actual["Estado"] = "Sin Cambios" #No realizamos cambios sobre estos dict
					for csv_data in anio_data_actual["csv"]:
						csv_data["Estado"] = "Sin Cambios" #Cambiamos el estado de los csv

				elif fecha_mod_anio_actual!=fecha_mod_anio_anterior:
					anio_data_actual["Estado"] = "Actualizar" #Realizamos Cambios sobre sus CSVs, verificamos los csv modificados y sus registros
					Existen_Cambios = True

					# ----------------------------------------------------->>>>>>>>>>>>>>>>>
					# Comparamos los csv de cada anio para ver cuales tienen modificasiones
					for csv_data_actual in anio_data_actual["csv"]:
						
						New_Data_Csv = True
						
						for csv_data_anterior in anio_data_anterior["csv"]:
							if csv_data_actual["nombre"] == csv_data_anterior["nombre"]:
								
								fecha_mod_csv_actual = csv_data_actual["fecha_modificasion"] + csv_data_actual["hora_modificasion"]
								fecha_mod_csv_anterior = csv_data_anterior["fecha_modificasion"] + csv_data_anterior["hora_modificasion"] 
								
								if fecha_mod_csv_actual == fecha_mod_csv_anterior:
									csv_data_actual["Estado"] = "Sin Cambios"

								elif fecha_mod_csv_actual != fecha_mod_csv_anterior:
									csv_data_actual["Estado"] = "Actualizar"
									Existen_Cambios = True

								New_Data_Csv = False
								break

						if New_Data_Csv == True:
							csv_data_actual["Estado"] = "Nuevo"
							Existen_Cambios = True
					# ----------------------------------------------------->>>>>>>>>>>>>>>>>
					# ----------------------------------------------------->>>>>>>>>>>>>>>>>

				New_Data_Anio = False
				break

		if New_Data_Anio == True:
			anio_data_actual["Estado"] = "Nuevo" #Agregamos el dict y agregamos los csvs y sus registros a la DB
			for csv_data in anio_data_actual["csv"]:
				csv_data["Estado"] = "Nuevo"
			Existen_Cambios = True
		
	return { "Existen_Cambios" : Existen_Cambios , "Data" : list_data_actual }


if __name__ == "__main__":
	
	list_data_anterior = retorna_ultima_actividad_generada( DIR_ACTUAL/"Historial_Datos_Troposfericos/" )

	#lista_registro = tratamiento_datos_data_productos_troposfericos( list_data_anterior )
	#Generador_de_JSON_Actividades_Mendoza( lista_registro , DIR_ACTUAL/"Historial_Datos_Troposfericos/" )
	'''
	json_data_actual = get_data_actualizada_productos_troposfericos()
	
	json_respuesta = comparacion_data_actual_con_data_anterior( list_data_anterior , json_data_actual["Datos"] )
	

	if json_respuesta["Existen_Cambios"] == True:
		print("Nuevos Registros")
		#Guardamos los datos en el historial
		#Realizamos los cambios en la DB
		
		#Gusardamos JSON en Historial
		Generador_de_JSON_Actividades_Mendoza( json_respuesta["Data"] , DIR_ACTUAL/"Historial_Datos_Troposfericos/" )
	else:
		print("Sin Cambios En los Registros")
	'''