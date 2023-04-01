import csv , pathlib


DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual


def generador_csv_file( headers , data , dir_carpeta_guardado , filename ):
    with open( dir_carpeta_guardado/filename , 'w', newline='' , encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)
    return dir_carpeta_guardado/filename


if __name__ == "__main__":
    headers = ['Nombre', 'Apellido', 'Edad']
    data = [ ['Juan', 'Pérez', 25], ['María', 'García', 30], ['Pedro', 'Sánchez', 35] ]
    
    generador_csv_file( headers , data , DIR_ACTUAL/"Files_CSV_Generados" , "file_csv_generado.csv" )