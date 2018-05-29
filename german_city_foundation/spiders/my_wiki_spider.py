import scrapy
import pandas as pd

class MyWikiSpiderSpider(scrapy.Spider):
    name = "my-wiki-spider"
    allowed_domains = ["https://de.wikipedia.org/"]
    start_urls = ['https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen']


    def parse(self, response):

    	staedte = pd.read_csv('./german_city_foundation/files/staedte.csv', encoding = "ISO-8859-1")
    	
    	ueberschrift = response.css('h1#firstHeading').extract_first()

    	if ueberschrift in staedte:
    		print('**' * 10, ' Stadt: ', ueberschrift)

    	else:
    		at_start_page = False
    		unterseiten = response.xpath('//div[@class="mw-parser-output"]/ul[1]/li/a/@href').extract()

    		if unterseiten is not None:
    			for j in unterseiten:
    				yield response.follow(j, callback=self.parse)

    	# Startseite:
    	# if response.request.url == 'https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen':
    	# 	for j in unterseiten:
    	# 		yield response.follow(j, callback=self.parse)
    	# elif 
    	# else:
    	# 	print("UNTERSEITE, erstmal nicht abgearbeitet: ", response.request.url)
    	

    	#print("*"*50)
    	#for l in links:
    	#	print('Ausgabe: ' + str(l))

    	#print("in parse Funktion")

if __name__ == "__main__":
	print("main")



''' To-Do:

Excel Datei mit allen Städten:
https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Aktuell/05Staedte.html

Als nächstes:
Stadtnamen zum Abgleich aus dieser Excel in eine Liste laden

staedte = pd.read_csv('staedte.csv', encoding = "ISO-8859-1")
'Arnis' in staedte['Staedte']

'''