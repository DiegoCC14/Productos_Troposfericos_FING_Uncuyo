from django.db import models


class Year( models.Model ):
	id = models.AutoField( primary_key=True )
	year = models.IntegerField()
	link = models.CharField( max_length=100 )


class Estaciones( models.Model ):
	id = models.AutoField( primary_key=True )
	nombre = models.CharField( max_length=30 )
	latitud = models.FloatField()
	longitud = models.FloatField()
	altura = models.FloatField( default=-1 )


class CSV_Files( models.Model ):
	id = models.AutoField( primary_key=True )
	nombre = models.CharField( max_length=30 )
	id_Estacion = models.ForeignKey( Estaciones , on_delete=models.CASCADE )
	id_Year = models.ForeignKey( Year , on_delete=models.CASCADE )
	ultima_modificasion = models.DateTimeField()
	peso = models.CharField( max_length=150 )
	link = models.CharField( max_length=100 )


class Registros_CSV( models.Model ):
	id = models.AutoField( primary_key=True )
	id_CSV = models.ForeignKey( CSV_Files , on_delete=models.CASCADE )
	#Datos Productos Troposfericos
	fecha = models.DateTimeField()
	presion = models.FloatField()
	temperatura = models.FloatField()
	IWV = models.FloatField()
	ZTD = models.FloatField()
	RMS_ERROR = models.FloatField()
	n_centros_procesamiento = models.FloatField()
	#------------------------>>>>>