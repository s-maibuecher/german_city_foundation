import scrapy

class MyWikiSpiderSpider(scrapy.Spider):
    name = "my-wiki-spider"
    allowed_domains = ["https://de.wikipedia.org/"]
    start_urls = ['https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen']

    def parse(self, response):

    	at_start_page = False

    	if response.request.url == 'https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen':
    		alle_jahrhundert_unterseiten = response.xpath('//div[@class="mw-parser-output"]/ul[1]/li/a/@href').extract()
    		for j in alle_jahrhundert_unterseiten:
    			print(j)
    	else:
    		print("*"*50)
    	

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

'''