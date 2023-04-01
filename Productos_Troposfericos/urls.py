
from django.contrib import admin
from django.urls import path
from .views import Actualizar_Datos_Troposfericos , Search_Data_Productos_Troposfericos , Productos_Troposfericos_Vista , Estaciones_Disponibles_API
from .views import descargar_csv_datos_requeridos , Panel_Administracion_View , Actualizar_Lat_Long_Altura_Productos_Troposfericos_API

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', Productos_Troposfericos_Vista.as_view() , name="productos_troposfericos_vista"),
    path('api_search_data_productos_troposfericos/', Search_Data_Productos_Troposfericos.as_view() , name="api_search_data_productos_troposfericos"),
    path('api_estaciones_disponibles/', Estaciones_Disponibles_API.as_view() , name="api_estaciones_disponibles"),

    path('descarga_csv_user/<str:nombre_csv>/', descargar_csv_datos_requeridos , name="api_estaciones_disponibles"),
    
    path('panel_administrador/', login_required( Panel_Administracion_View.as_view() ) , name="panel_administrador"),
    path('actualizar_datos_troposfericos/', login_required( Actualizar_Datos_Troposfericos.as_view() ) , name="actualizar_datos_troposfericos"),
    path('actualizar_lat_long_alt_estaciones_datos_troposfericos/', login_required( Actualizar_Lat_Long_Altura_Productos_Troposfericos_API.as_view() ) , name="actualizar_lat_long_alt_estaciones_datos_troposfericos"),    
]
