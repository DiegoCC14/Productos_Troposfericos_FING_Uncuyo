import requests , pathlib , csv , urllib.parse , os
from urllib.parse import urlparse
#import urllib.request

DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual


def descargar_csv( url_csv , dir_carpeta_guardado ):
    try:
        respuesta = requests.get( url_csv )
        nombre_archivo = urlparse( url_csv ).path.split('/')[-1]

        with open( dir_carpeta_guardado/nombre_archivo , 'wb') as f:
            f.write(respuesta.content)
        print( f'¡Descarga CSV {nombre_archivo} completada!' )
        return True
    except:
        return False


def leer_csv_desde_url( url_csv ):
    registros = []
    with urllib.request.urlopen( url_csv ) as response:
        datos = response.read().decode('utf-8')
        lector = csv.reader(datos.splitlines(), delimiter=',')
        encabezados = next(lector, None)
        for registro in lector:
            registros.append(registro)
    return registros

def leer_csv_file( dir_csv_file ):
    with open( dir_csv_file ) as csv_file:
        lector = csv.reader( csv_file , delimiter=',')
        encabezados = next(lector, None)
        registros = [ registro for registro in lector ]
    return registros

def obtener_csv_de_directorio( ruta_carpeta ):
    archivos = os.listdir(ruta_carpeta)
    return [archivo for archivo in archivos if archivo.endswith('.csv')]

if __name__ == "__main__":

    #print( leer_csv_file( DIR_ACTUAL/"CSV_Temporales/3ARO_13.csv" ) )
    print( obtener_csv_de_directorio( DIR_ACTUAL/"CSV_Temporales" ) )
    list_csv = obtener_csv_de_directorio( DIR_ACTUAL/"CSV_Temporales" )
    for name_csv in list_csv:
        lista_csv = leer_csv_file( DIR_ACTUAL/f"CSV_Temporales/{name_csv}" )
        for registro in lista_csv:
            #print( len(registro) )
            registro[0]
            float(registro[1])
            float(registro[2])
            float(registro[3])
            float(registro[4])
            float(registro[5])
            float( registro[6] )
            if len(registro) != 7:
                print("Error Lista Longitud")
    '''
    url_csv = "https://cima.ingenieria.uncuyo.edu.ar/IWV_ERA5/productos/anual_2013/25MA_13.csv"
    registros_csv = leer_csv_desde_url( url_csv )
    for registro in registros_csv:
        print( registro )

    url_csv = "https://cima.ingenieria.uncuyo.edu.ar/IWV_ERA5/productos/anual_2012/ABCC_12.csv"
    registros_csv = leer_csv_desde_url( url_csv )
    for registro in registros_csv:
        print( registro )

    url_csv = 'https://cima.ingenieria.uncuyo.edu.ar/IWV_ERA5/productos/anual_2012/ABPD_12.csv'
    registros_csv = leer_csv_desde_url( url_csv )
    for registro in registros_csv:
        print( registro )
    '''