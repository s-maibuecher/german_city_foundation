import scrapy
import pandas as pd

class MyWikiSpiderSpider(scrapy.Spider):
    name = "my-wiki-spider"
    allowed_domains = ["wikipedia.org"]
    start_urls = ['https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen']

    custom_settings = {
        'DEPTH_LIMIT': 2
    }


    def parse(self, response):

    	staedte = pd.read_csv('./german_city_foundation/files/staedte.csv', encoding = "ISO-8859-1")

    	#print('############', 'Stuttgart' in staedte['Staedte']) # klappt
    	
    	ueberschrift = response.xpath('//h1[@id="firstHeading"]/text()').extract_first()

    	with open('my_log.txt','a') as f:
    		f.write(ueberschrift)
    		f.write('\n')
    		if ueberschrift in staedte:
    			f.write('##################################\n')

    	if ueberschrift in staedte:
    		#print('**' * 10, ' Stadt: ', ueberschrift)
    		# with open('my_log.txt','wb') as f:
    		# 	f.write('Stadt: ')
    		# 	f.write(ueberschrift)
    		pass

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

USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling


'''