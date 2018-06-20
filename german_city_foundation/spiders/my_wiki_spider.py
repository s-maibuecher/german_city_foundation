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

    		## Wie gehe ich mit den Koordinaten um?

    		'''
    		Tiefe 2:Aschersleben ['
    		<span id="coordinates" class="coordinates plainlinks-print">
    		<span title="Koordinatensystem WGS84">Koordinaten: </span>
    		<a class="external text" href="//tools.wmflabs.org/geohack/geohack.php?pagename=Aschersleben&amp;language=de&amp;params=51.755555555556_N_11.455555555556_E_region:DE-ST_type:city(27751)">
    		<span title="Breitengrad">51°\xa045′\xa0<abbr title="Nord">N</abbr></span>,
    		<span title="Längengrad">11°\xa027′\xa0<abbr title="Ost">O</abbr></span></a></span>']

    		'''
    	
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
    				

    	with open('my_log.txt','w') as f:
    		f.write(ueberschrift)
    		f.write('\t')
    		f.write(str(response.meta["depth"]))
    		f.write('\n')

    	if unterseiten.xpath('./a').extract() is not None:
    		for u in unterseiten.xpath('./a/@href').extract():
    			yield response.follow(u, callback=self.parse)


if __name__ == "__main__":
	print("main")



''' To-Do:

Meta Informationen übergeben:
http://www.scrapingauthority.com/scrapy-meta

Excel Datei mit allen Städten:
https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Aktuell/05Staedte.html

Als nächstes:
Wie gehe ich mit den Koordinaten um?
Daten in Datenbank speichern

USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling


'''