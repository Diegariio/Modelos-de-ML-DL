import requests
from bs4 import BeautifulSoup
import openpyxl

workbook = openpyxl.Workbook() # Creamos un nuevo libro de trabajo de Excel
hoja_activa = workbook.active # Seleccionamos la hoja activa

# tr hace referencia a la etiqueta <tr> del HTML de la página, es decir las filas.
# td hace referencia a la etiqueta <td> del HTML de la página, es decir las columnas.

# -------------------------------------------------------- Recopila los datos de la página en un array --------------------------------------------------------
data = [] # Almacenará cada dato de la tabla completa en un arreglo de elementos para luego añadirlos a un archivo en formato 'xlsx' (excel).
for year in range(2023, 1969, -1): # Año del 2023 al 2020 con un decremento de 1
    for month in range(4, 10, +1): # Meses del 1 al 12 con un incremento de 1
        url = f'https://climatologia.meteochile.gob.cl/application/mensual/viento10DireccionesMensual/360019/{year}/{month}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        elementos_tr = soup.find_all('tr', class_='text-center') # Recopila todas las etiquetas <tr> con clase 'text-center' del HTML
        elementos_tr = [tr for tr in elementos_tr if tr.get('class') == ['text-center']]

        # Se ocupa una matriz para recorrer la tabla. Donde 'tr' son las filas y 'td' es la columna de cada fila.
        for tr in elementos_tr: # Se recorren todas las filas
            elementos_td = tr.find_all('td') # Busca y asigna todos aquellos resultados con la etiqueta '<td>'
            
            index = 0 # Este indice se ocupa para luego poder cambiar el formato del dia. Prácticamente guarda el número de la fila. Se asigna a 0 por cada iteración de las columnas recorridas.
            for td in elementos_td: # Se recorren todas las columnas
                td = td.get_text().strip() # Obtiene en formato texto el valor contenido en la columna. 'strip()' elimina los posibles espacios que se puedan generar
                if td == '':
                    td = 'xd'
                if td == '.':
                    td = 'xd'
                if td == 'Horario':
                    break
                if td == '12 UTC':
                    break
                if td == '18 UTC':
                    break
                if td == '00 UTC':
                    break
                if td == '121800 UTC':
                    break
                day = td # Paso el dato obtenido a la variable 'day' para que a la hora de darle el formato se vea mejor visualmente.
                if index == 0: # Si el índice es '0'. Es decir, es la primera columna de la tabla se va a modificar el formato de la fecha
                    td = f"{day}-{month}-{year}"

                data.append(td) # Agrega el dato recopilado de la página al arreglo de elementos
                index += 1 # Se incrementa el índice ya que cambia el valor de la columna 

# -------------------------------------------------------- Convierte los datos del array al excel --------------------------------------------------------
row = 1 # Inicializa las filas en 1. Excel requiere que las filas comiencen en 1.
col = 1 # Inicializa las columnas en 1. Excel requiere que las columnas comiencen en 1.
for i in range(len(data)): # Recorre los datos según la cantidad de datos del array.
    hoja_activa.cell(row=row, column=col, value=data[i]) # Asigna los datos del array en el excel
    col += 1 # Por cada asignación, debe ir aumentando las columnas 
    if (((i + 1) % 16) == 0): # [1]
        row += 1
        col = 1
    
# Guardamos el libro de trabajo en un archivo
workbook.save("agua-caida.xlsx")

# [1]: Dado que el array de datos recopilados es lineal, no hay un índice para que el programa sepa cuando es fila y cuando es columna.
#      Por lo tanto se ocupa esta operación para que cuando llegue a la 'columna 7' pase a convertirse en la columna 1 de la siguiente fila.
#      El número 7 puede variar según la cantidad de columnas de la página a la cual se le esté realizando scraping