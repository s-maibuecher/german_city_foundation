import scrapy
import pandas as pd
import re

import sqlite3



class MyWikiSpiderSpider(scrapy.Spider):
    name = "my-wiki-spider"
    allowed_domains = ["wikipedia.org"]
    start_urls = ['https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen']

    custom_settings = {
        'DEPTH_LIMIT': 2
    }


    # create the table
    sqlite_file = './my_city_db.sqlite'
    con = sqlite3.connect(sqlite_file)
    cur = con.cursor()

    cur.execute(''' CREATE TABLE IF NOT EXISTS CityTable( city TEXT PRIMARY KEY, gruendungsjahr INT, breitengrad TEXT, laengengrad TEXT, jahr_sollte_ueberprueft_werden INT );''')
    con.commit()

    def parse(self, response):

    	staedte = pd.read_csv('./german_city_foundation/files/staedte.csv', encoding = "ISO-8859-1")

    	unterseiten = response.xpath('//div[@class="mw-parser-output"]/ul[1]/li')

    	# Stadtseiten sind nur auf Tiefe 2 verfügbar:
    	if response.meta["depth"] == 2:

    		ueberschrift = response.xpath('//h1[@id="firstHeading"]/text()').extract_first()
    		# Koordinaten auslesen
    		#print('Tiefe 2:')
    		koordinaten = response.xpath('//*[@id="coordinates"]')
    		#print(ueberschrift)
    		#print("META", str(response.meta['jahr']))

    		if ueberschrift in staedte['Staedte'] and koordinaten:

    			breitengrad = koordinaten.xpath('descendant::*[@title="Breitengrad"]/text()').extract_first()
    			laengengrad = koordinaten.xpath('descendant::*[@title="Längengrad"]/text()').extract_first()


    			self.cur.execute("INSERT OR IGNORE INTO CityTable VALUES ( ?, ?, ?, ?, ?) ", ( ueberschrift, response.meta['jahr'], breitengrad, laengengrad, response.meta['jahr_unsicher']))
    			self.con.commit()


    	elif response.meta["depth"] == 1:
    		#Jahrhundertseite: hier untersuchen, ob der Link eine Stadt enthält, wenn dann Stadt und Gründungsdatum abfangen:
    		#print('Tiefe 1:')
    		ueberschrift = response.xpath('//h1[@id="firstHeading"]/text()').extract_first()

    		if unterseiten.xpath('./a').extract() is not None:
    			for li in unterseiten:

    				jahr_unsicher = 0
    				
    				gruendungsjahr = None
    				temp_stadtname = None
    				
    				for a in li.xpath('a'):
    					m = re.search('(\d+)(\/\d+)?(\s*v\.\s*Chr\.)?', str(a.xpath('./text()').extract_first()))
    					#print('*** DEBUG INFO: a text', str(a.xpath('./text()').extract_first()))
    					if m:
    						if m.group(3) is not None:
    							gruendungsjahr = -1 * int(m.group(1))
    						else:
    							gruendungsjahr = int(m.group(1))
    					
    				# Found no number within the link text, maybe there is a number (the year of foundation), which is not linked??
    				if gruendungsjahr is None:
    					# noch eine Spalte "Jahr unklar?" die dann mit 1 füllen wenn dem so ist und die ganze li Zeile reinkopieren?
    					# oder besser noch Überschrift von der Zwischenseite beachten und Zahlenwerte vergleichen
    					#print('*** DEBUG INFO: gruendungsjahr is None', str(li))
    					jahr_unsicher = 1 # value := 1 if scrawlt year is uncertain

    					regex_jahrhundert_in_ueberschrift = re.search('(\d+)\.(\s*v\.\s*Chr\.)?', ueberschrift)
    					#print('*** DEBUG INFO: gruendungsjahr is None', str(regex_jahrhundert_in_ueberschrift.group(1)))
    					jahrhundert_in_ueberschrift = None
    					if regex_jahrhundert_in_ueberschrift:
    						if regex_jahrhundert_in_ueberschrift.group(2) is not None:
    							jahrhundert_in_ueberschrift = -1 * int(regex_jahrhundert_in_ueberschrift.group(1))
    						else:
    							jahrhundert_in_ueberschrift = int(regex_jahrhundert_in_ueberschrift.group(1))

    							# hier oben Print Debug Ausgaben reinsetzen


    					all_li_text = li.xpath('./text()').extract()
    					li_string = ''
    					for l in all_li_text:
    						li_string += l + " "

    					regex_search_year_in_li = re.findall('(\d+)[\/\d+]?', li_string)
    					#print('#'*20, regex_search_year_in_li) # hier weiter debug meldungen runtergeben
    					range_the_year_should_be_in_min = 100 * jahrhundert_in_ueberschrift
    					range_the_year_should_be_in_max = 100 * jahrhundert_in_ueberschrift + 100

    					for y in regex_search_year_in_li:
    						if int(y) >= range_the_year_should_be_in_min and int(y) <= range_the_year_should_be_in_max:
    							gruendungsjahr = int(y)

    					
    				for a in li.xpath('a'):
    					if a.xpath('./text()').extract_first() in staedte['Staedte']: # Gehen mit dem Abgleich Städte flöten??
    						temp_stadtname = a.xpath('./text()').extract_first()

    					yield response.follow(a.xpath('@href').extract_first(), callback=self.parse, meta={'jahr' : gruendungsjahr, 'jahr_unsicher': jahr_unsicher})


    	# Generate Follow Links for Start URL (response.meta["depth"] == 0):
    	if response.meta["depth"] == 0 and unterseiten.xpath('./a').extract() is not None:
    		for u in unterseiten.xpath('./a/@href').extract():
    			yield response.follow(u, callback=self.parse)


    def closeDB(self):
    	self.con.close()


    def __del__(self):
    	print("Datenbank ausgeben:")
    	self.cur.execute("SELECT * FROM CityTable LIMIT 5")
    	all_rows = self.cur.fetchall()
    	print('1):', all_rows)
    	self.con.commit()
    	print('DATENBANK WIRD GESCHLOSSEN.')
    	self.closeDB()
    	
''' To-Do:

Meta Informationen übergeben:
http://www.scrapingauthority.com/scrapy-meta

Excel Datei mit allen Städten:
https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Aktuell/05Staedte.html

Als nächstes:

Datenbankabfragen mit Fehlerbehandlung ausführen


USER_AGENT Bot Einstellungen noch vornehmen
https://eliteinformatiker.de/2017/10/15/verantwortungsvolles-crawling


'''