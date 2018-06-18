import scrapy
import pandas as pd
import re

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

    	unterseiten = response.xpath('//div[@class="mw-parser-output"]/ul[1]/li')

    	# Stadtseiten sind nur auf Tiefe 2 verfügbar:
    	if response.meta["depth"] == 2:
    		# Koordinaten auslesen
    		print('Tiefe 2:')
    		koordinaten = response.xpath('//*[@id="coordinates"]').extract()
    		print(ueberschrift, koordinaten)
    	
    	elif response.meta["depth"] == 1:
    		#Jahrhundertseite: hier untersuchen, ob der Link eine Stadt enthält, wenn dann Stadt und Gründungsdatum abfangen:
    		print('Tiefe 1:')
    		if unterseiten.xpath('./a').extract() is not None:
    			for li in unterseiten:
    				#if u in staedte['Staedte']:
    				#print('STADT: '  + u)

    				### hier weiter:
    				# wenn der zugehörige Linktext eine Stadt ist, dann vergleich die Nachbarlinks auf Zahlenwert
    				# oder das Muster "X v. Chr."
    				# gebe diese Werte aus

    				### gucken, wie man die Selector objects weiter verwenden kann:
    				# https://doc.scrapy.org/en/latest/topics/selectors.html#scrapy.selector.Selector
    				temp_stadtname = None
    				temp_gruendungsjahr = None
    				for a in li.xpath('a/text()').extract():
    					m = re.search('(\d+)(\s*v\.\s*Chr\.)?', a)
    					if m:
    						#print('Reg-Ausdruck passt: ', m.group(0), ' ', m.group(1), m.group(2))
    						if m.group(2) is not None:
    							temp_gruendungsjahr = -1 * int(m.group(1))
    						else:
    							temp_gruendungsjahr = int(m.group(1))
    					elif a in staedte['Staedte']:
    						temp_stadtname = a
    				print(ueberschrift, temp_stadtname, temp_gruendungsjahr)
    				

    	with open('my_log.txt','a') as f:
    		f.write(ueberschrift)
    		f.write('\t')
    		f.write(str(response.meta["depth"]))
    		f.write('\n')

    	if unterseiten.xpath('./a').extract() is not None:
    		for u in unterseiten.xpath('./a/@href').extract():
    			yield response.follow(u, callback=self.parse)

    	# with open('my_log.txt','a') as f:
    	# 	f.write(ueberschrift)
    	# 	f.write('\n')
    	# 	if ueberschrift in staedte['Staedte']:
    	# 		f.write('##################################\n')
    	# 		f.write(str(response.meta["depth"]))
    	# 		f.write('****\n')

    	# if ueberschrift in staedte['Staedte']:
    	# 	#print('**' * 10, ' Stadt: ', ueberschrift)
    	# 	# with open('my_log.txt','wb') as f:
    	# 	# 	f.write('Stadt: ')
    	# 	# 	f.write(ueberschrift)
    	# 	pass

    	# else:
    	# 	#at_start_page = False
    	# 	unterseiten = response.xpath('//div[@class="mw-parser-output"]/ul[1]/li/a/@href').extract()

    	# 	if unterseiten is not None:
    	# 		for j in unterseiten:
    	# 			yield response.follow(j, callback=self.parse)


if __name__ == "__main__":
	print("main")



''' To-Do:

Meta Informationen übergeben:
http://www.scrapingauthority.com/scrapy-meta

Excel Datei mit allen Städten:
https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Aktuell/05Staedte.html

Als nächstes:
Tiefe 2 wird noch nicht wie erwünscht gecrawlt

USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling


'''