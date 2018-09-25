from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sqlite3


def coolerProjections():
    #m = Basemap(projection='mill',llcrnrlat=47.1,urcrnrlat=55.2, llcrnrlon=5.5,urcrnrlon=15.3, resolution='l')
    m = Basemap(width=12000000,height=9000000,projection='lcc', resolution='l',lat_1=5,lat_2=6,lat_0=52,lon_0=9)

    #m.drawcountries(linewidth=1.5)
    #m.drawcoastlines(linewidth=1.5)
    #m.drawstates()


    #m.bluemarble()

    m.etopo()

    plt.title("GCF")
    plt.show()

    #plt.savefig('map.png')


#https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python


# are you getting an error like:
# ImportError: The _imaging C module is not installed
# This meanss you have PIL, but you have the wrong bit version.
# If it says you don't have PIL at all, then you better go grab it
# but this should have come with your matplotlib installation.


def loadSqlEntries():
	connection = sqlite3.connect("first_valid_db.sqlite")
	cursor = connection.cursor()

	cursor.execute("SELECT * FROM CityTable LIMIT 5;") 
	print("\nfetch one:")
	res = cursor.fetchall() #cursor.fetchone() 
	print(res)

#coolerProjections()
loadSqlEntries()
