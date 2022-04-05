import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'file:///C:/Users/Francisco/Documents/Programación/Projects_Pythom/Python-basico-07/paginas/Provincia_de_Loja.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'cantones_loja.csv' # Nombre del archivo
        tablas = response.xpath("//table[@class='wikitable']") # Selector de todas las tablas
        tabla = tablas[5] # Almacena la tabla que se trabajará
        lista = tabla.xpath("tbody/tr/td/b/a/text()").getall() # Almacena los nombres de los cantones
        data = pd.DataFrame(lista, columns = ["Cantones"]) # Convierte la lista en un dataframe
        data.to_csv(filename) # Exporta el dataframe en un CSV