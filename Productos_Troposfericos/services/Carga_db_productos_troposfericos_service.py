from models.models import Year , Estaciones , CSV_Files , Registros_CSV #Models Djangom ORM

from .Scraping_productos_troposfericos_service import get_data_actualizada_productos_troposfericos , comparacion_data_actual_con_data_anterior , tratamiento_datos_data_productos_troposfericos
from .Generador_de_JSON_service import retorna_ultima_actividad_generada , Generador_de_JSON_Actividades_Mendoza
from .Descarga_CSV import leer_csv_desde_url , descargar_csv , leer_csv_file
import pathlib , requests , time
import threading , datetime

from concurrent.futures import ThreadPoolExecutor , as_completed


DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual


def actualizar_db_productos_troposfericos():

	Dir_Historial_Productos = DIR_ACTUAL/"Historial_Datos_Troposfericos/"

	list_data_anterior = retorna_ultima_actividad_generada( Dir_Historial_Productos )
	json_data_actual = get_data_actualizada_productos_troposfericos() #Obtenemos los datos actualizados de la pagina oficial
	json_data_actual["Datos"] = tratamiento_datos_data_productos_troposfericos( json_data_actual["Datos"] )
	
	print( f"Lista Antiorio {list_data_anterior[0]['fecha_modificasion']}"  )

	json_respuesta = comparacion_data_actual_con_data_anterior( list_data_anterior , json_data_actual["Datos"] ) #Comparamos los datos con los anteriores
	
	if json_respuesta["Existen_Cambios"] == True:

		print("~~>> Nuevos Registros Agregados")

		#Guardamos los datos en el historial
		#Realizamos los cambios en la DB
		#json_respuesta["Data"] = json_respuesta["Data"][ len( json_respuesta["Data"] )-5 : len( json_respuesta["Data"] )-4 ] #Solo tomamos los 2 elementos primeros

		for data_year in json_respuesta["Data"]:
			
			print( f"Procesando Year: {data_year['nombre']}")

			if data_year["Estado"] == "Nuevo" or data_year["Estado"] == "Actualizar": #Tenemos nuevos datos Year  

				num_year = int( data_year["nombre"].replace("anual_","").replace("/","") )
				#Registro Year ya Creado ---------------------->>>>>>>>>>>>>>>>>>
				if data_year["Estado"] == "Nuevo" and not( Year.objects.filter( year=num_year ).exists() ): #Agregamos si el anio no existe
					Year( year=num_year , link= data_year["link"] ).save() #Luego lo guardamos
				
				obj_year = Year.objects.filter( year=num_year )[0]
				#----------------------==---------------------->>>>>>>>>>>>>>>>>>

				cantidad_hilos_maximos = 10
				list_futures_descarga_csv = []

				#data_year["csv"] = data_year["csv"][0:4]

				with ThreadPoolExecutor( max_workers=cantidad_hilos_maximos ) as executor:
					for data_csv in [ data_csv_valida for data_csv_valida in data_year["csv"] if data_csv_valida["Estado"] == "Nuevo" or data_csv_valida["Estado"] == "Actualizar" ]:
						# Descargamos los csv y agregamos el campo ubicasion a el diccionario
						list_futures_descarga_csv.append( executor.submit( descargar_csv , data_csv["link"] , DIR_ACTUAL/"CSV_Temporales" ) )
						# --------------------------------------------------->>>>>>>>>>>>>>>>
				print("Futures Descarga CSV Terminado ---------->>>>>>>>>>> ")
				
				for contador,data_csv in enumerate( [ data_csv_valida for data_csv_valida in data_year["csv"] if data_csv_valida["Estado"] == "Nuevo" or data_csv_valida["Estado"] == "Actualizar" ] ):
					print( f'PROCESANDO {data_csv["nombre"]} - {contador}: de {len([ data_csv_valida for data_csv_valida in data_year["csv"] if data_csv_valida["Estado"] == "Nuevo" or data_csv_valida["Estado"] == "Actualizar" ])}' )
					guardando_en_db_datos_csv_y_registro(data_csv , obj_year)
			
		#Gusardamos JSON en Historial
		Generador_de_JSON_Actividades_Mendoza( json_respuesta["Data"] , DIR_ACTUAL/"Historial_Datos_Troposfericos/" )
		
		return( {"Mensaje": "Proceso Finalizado Correctamente - Nuevos Registros"} )

	else:
		return( {"Mensaje": "Proceso Finalizado Correctamente - Sin Registros Nuevos"} )

def guardando_en_db_datos_csv_y_registro( data_csv , obj_year_model ):
	
	try:
		nombre_estacion = data_csv["nombre"][0:4] #nombre Estacion, lo creamos si no existe
		#Registro Estacion ya Creado ---------------------->>>>>>>>>>>>>>>>>>
		if not( Estaciones.objects.filter( nombre=nombre_estacion ).exists() ): #La estacion no existe, la ingresamos
			Estaciones(
				nombre=nombre_estacion,
				latitud=50.02632, #Luego cambiamos la Latitud y Longitud
				longitud=15.02634).save()

		obj_estacion = Estaciones.objects.filter( nombre=nombre_estacion )[0]
		#----------------------==---------------------->>>>>>>>>>>>>>>>>>
		
		nombre_csv = data_csv["nombre"].replace(".csv","")
		if CSV_Files.objects.filter( nombre=nombre_csv ).exists():
			CSV_Files.objects.filter( nombre=nombre_csv ).delete() #Borramos el elemento y por cascada se eliminan sus registros
		
		#Creamos el elemento CSV y agregamos sus registros actualizados
		CSV_Files(
			nombre=nombre_csv,
			id_Estacion=obj_estacion,
			id_Year=obj_year_model,
			ultima_modificasion=f'{data_csv["fecha_modificasion"]} {data_csv["hora_modificasion"]}',
			peso=data_csv["peso_kbits"] ,
			link=data_csv["link"] 
			).save()
		
		obj_csv_file = CSV_Files.objects.filter( nombre=nombre_csv , id_Estacion=obj_estacion , id_Year=obj_year_model )[0]

		list_registros_csv = leer_csv_file( DIR_ACTUAL/f"CSV_Temporales/{nombre_csv}.csv" )

		lista_obj_registros_csv = []
		for registro_csv in list_registros_csv:
			lista_obj_registros_csv.append( Registros_CSV(
				id_CSV = obj_csv_file, fecha = registro_csv[0] ,
				presion = registro_csv[1], temperatura = registro_csv[2],
				IWV = registro_csv[3], ZTD = registro_csv[4],
				RMS_ERROR = registro_csv[5], n_centros_procesamiento = registro_csv[6] ) )
		
		Registros_CSV.objects.bulk_create( lista_obj_registros_csv )

		return ( obj_csv_file,[] )

	except:
		print("ERROR EN PROCESO ~~~~~~~~~~~~>>>>>>>>>>")
		print("ERROR EN PROCESO ~~~~~~~~~~~~>>>>>>>>>>")


if __name__ == "__main__":
	carga_db_productos_troposfericos()
