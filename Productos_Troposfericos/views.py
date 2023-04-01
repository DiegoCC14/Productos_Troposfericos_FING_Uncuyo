import os , json , pathlib , time

from .services.Carga_db_productos_troposfericos_service import actualizar_db_productos_troposfericos
from .services.Generador_CSV_service import generador_csv_file


from models.models import Year , Estaciones , CSV_Files , Registros_CSV #Models Djangom ORM

from django.http import JsonResponse , HttpResponse
from django.shortcuts import render , redirect
from django.views import View

from concurrent.futures import ThreadPoolExecutor , as_completed

DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual


class Actualizar_Datos_Troposfericos( View ):

	def get( self , request ):
		mensaje_actualizacion = actualizar_db_productos_troposfericos()
		return JsonResponse( mensaje_actualizacion )


class Productos_Troposfericos_Vista( View ):

	def get( self , request ):
		return render( request , "productos_troposfericos.html" )


class Estaciones_Disponibles_API( View ):
	
	def get( self , request ):
		estaciones_list = [{"nombre":estacion.nombre,"latitud":estacion.latitud,"longitud":estacion.longitud} for estacion in Estaciones.objects.all()]
		return JsonResponse( {"Estaciones": estaciones_list } )	


def serializacion_registros( obj_registros , lista_registros_serializados ):
	for data in obj_registros:
		lista_registros_serializados.append( [str(data.fecha),str(data.presion),str(data.temperatura),str(data.IWV),str(data.ZTD),str(data.RMS_ERROR),str(data.n_centros_procesamiento)] )
	print("Proceso Finalizado~~~>>>") 


class Search_Data_Productos_Troposfericos( View ):

	def get( self , request ):
		data_request = request.GET.dict()
		data_search = json.loads( data_request["data"] )
		lista_csv_generados = []
		registros_lista = []
		for nombre_estacion in data_search["estaciones"]:	
			registros_encontrados = Registros_CSV.objects.filter( id_CSV__id_Estacion__nombre=nombre_estacion , fecha__range=(data_search["fecha_desde"] , data_search["fecha_hasta"]) )
			registros_lista.append( {'nombre':nombre_estacion , 'registros':registros_encontrados , 'lista_registros_serializados':[] } )
		
		list_futures_descarga_csv = []
		with ThreadPoolExecutor( max_workers=15 ) as executor:
			for dicc_registro_db in registros_lista:
				nombre =dicc_registro_db["nombre"]
				data = dicc_registro_db["registros"]
				lista_registros_serializados = dicc_registro_db["lista_registros_serializados"]
				list_futures_descarga_csv.append( executor.submit( serializacion_registros , data , lista_registros_serializados ) )
		

		contador = 0
		data_search["headers"] = ["fecha"] + data_search["headers"] + ["RMS_ERROR","n"] #Allgunas cabezeras agregadas
		for puntero , cabezera in enumerate( ["fecha","presion","temperatura","IWV","ZTD","RMS_ERROR","n"] ):
			#[ fecha, presion, temperatura, IWV, ZTD, RMS_ERROR, n_centros_procesamiento] DB Serializadoe
			if not( cabezera in data_search["headers"] ) :
				for dicc_registro_db in registros_lista:
					for lista_registro in dicc_registro_db["lista_registros_serializados"]: 
						lista_registro.pop(puntero-contador)
				contador+=1
		

		for dicc_registro_db in registros_lista:
			nombre_estacion = dicc_registro_db["nombre"]
			registro_csv = dicc_registro_db["lista_registros_serializados"]
			filename_csv = f'{nombre_estacion}_{data_search["fecha_desde"].replace(":","_")}__{data_search["fecha_hasta"].replace(":","_")}.csv'
			generador_csv_file( data_search["headers"] , registro_csv , DIR_ACTUAL/f'static/CSV_Usuarios_Temporales' , filename_csv )
			lista_csv_generados.append( {"name": filename_csv.replace(".csv","") } )
		
		return JsonResponse( {"csvs_generados": lista_csv_generados } )


def descargar_csv_datos_requeridos( request , nombre_csv ):
	with open( DIR_ACTUAL/f'static/CSV_Usuarios_Temporales/{nombre_csv}.csv', 'r') as f:
		csv_file = f.read()
		# Se crea una respuesta HTTP con el archivo CSV
		response = HttpResponse(csv_file, content_type='text/csv')
		response['Content-Disposition'] = f'attachment; filename="{nombre_csv}.csv"'
	pathlib.Path.unlink( DIR_ACTUAL/f'static/CSV_Usuarios_Temporales/{nombre_csv}.csv' )
	return response


class Panel_Administracion_View( View ):

	def get( self , request ):
		return render( request , "administrador.html")

import pandas as pd

class Actualizar_Lat_Long_Altura_Productos_Troposfericos_API( View ):
	
	def post( self , request ):
		#EstacionModel: nombre , latitud , longitud , altura
		CSV_EstacionLatLongAlt = request.FILES.get( "CSV_EST_LAT_LONG_ALT" )
		df = pd.read_csv( CSV_EstacionLatLongAlt , sep=';', encoding='utf-8')
		
		estacion_update = []
		for registro in df.values.tolist():
			# nombre: registro[0] , latitud = registro[1] , longitud = registro[2] , altura = registro[3]
			obj_estacion = Estaciones.objects.filter( nombre=registro[0] )
			if obj_estacion.exists():
				obj_estacion = obj_estacion[0]
				obj_estacion.longitud = registro[1]
				obj_estacion.latitud = registro[2]
				obj_estacion.altura = registro[3]
				estacion_update.append( obj_estacion )

		Estaciones.objects.bulk_update( estacion_update , ['latitud' , 'longitud' , 'altura'])

		return JsonResponse( {"csvs_generados": "funcando" } )	