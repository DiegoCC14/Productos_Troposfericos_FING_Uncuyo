from models.models import Year , Estaciones , CSV_Files , Registros_CSV #Models Djangom ORM

from django.contrib import admin

def imagen(self, obj):
	return format_html('<img src="{}" />'.format( obj.image.url ))

#image_tag.short_description = 'Image'

@admin.register( Year )
class YearAdmin(admin.ModelAdmin):
	list_display = ( "id" ,"year", "link")


@admin.register( Estaciones )
class EstacionesAdmin(admin.ModelAdmin):
	list_display = ( "id","nombre", 'latitud', 'longitud' , 'altura')


@admin.register( CSV_Files )
class CSV_FilesAdmin(admin.ModelAdmin):
	list_display = ( "id","nombre", "id_Estacion", "id_Year", "ultima_modificasion", "link")


@admin.register( Registros_CSV )
class Registros_CSVAdmin(admin.ModelAdmin):
	list_display = ( 'id','id_CSV','fecha','presion', "temperatura" ,'IWV','ZTD', 'RMS_ERROR' , 'n_centros_procesamiento' )
