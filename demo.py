import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://es.wikipedia.org/wiki/Provincias_de_Ecuador',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'provincias_ecuador1.csv' # Nombre del archivo
        trs = response.xpath("""//table[@class='sortable']/tbody/tr""") # Selector de todos los tr
        lista = [] # Lista vacía
        for t in trs: # Recorre los tr
            lista_td = t.xpath("td") # Almacena los td que contenga el tr en cuestión
            
            if(len(lista_td)==13): # Verifica si hay tds
                poblacion = lista_td[0].xpath("text()").get() # Obtiene el texto del primer td
                area = lista_td[1].xpath("text()").get() # " " " " " " segundo "
                densidad = lista_td[2].xpath("text()").get() # " " " " " " tercer "
                provincia = lista_td[3].xpath("a/text()").get() # " " " " " " cuarto " que se encuentra dentro de una etiqueta "a"
                habitantes = lista_td[4].xpath("text()").get().replace("\xa0", " ") # " " " " " " quinto " reemplanzando el código por el espacio
                area1 = lista_td[5].xpath("text()").get() # " " " " " " sexto "
                densidad1 = lista_td[6].xpath("text()").get() # " " " " " " séptimo "
                cantones = lista_td[7].xpath("text()").get() # " " " " " " octavo "
                fundacion = lista_td[8].xpath("text()").get() # " " " " " " noveno "
                bandera = lista_td[9].xpath("span/a/@href").get() # Obtiene la url de la bandera del décimo td que se encuentra dentro de un "span" y una "a"
                capital = lista_td[10].xpath("a/text()").get() # Obtiene el texto del onceavo td que se encuentra dentro de una etiqueta "a"
                habitantes1 = lista_td[11].xpath("text()").get().replace("\xa0", " ") # Obtiene el texto del doceavo td reemplanzando el código por el espacio
                numero = lista_td[12].xpath("text()").get().replace("\n", "") # Obtiene el texto del treceavo td reemplanzando el salto de línea por vacio

                # Almacena en una lista, diccionarios que contengan los datos extraidos de los tds
                lista.append({'población':poblacion, 'área':area, 'densidad':densidad,
                    'provincia':provincia, 'habitantes (2020)':habitantes, 'área (km^2)':area1,
                    'densidad (hab./km^2)': densidad1, 'cantones':cantones, 'fundación':fundacion,
                    'bandera':bandera, 'capital':capital, 'habitantes (2010)':habitantes1,
                    'número':numero})
        data = pd.DataFrame.from_dict(lista) # Convierte la lista de diccionarios en un dataframe
        data.to_csv(filename, index=False) # Exporta el dataframe en un CSV, sin guardar el index