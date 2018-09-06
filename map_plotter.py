from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np



def coolerProjections():
    #m = Basemap(projection='mill',llcrnrlat=47.1,urcrnrlat=55.2, llcrnrlon=5.5,urcrnrlon=15.3, resolution='l')
    m = Basemap(width=12000000,height=9000000,projection='lcc', resolution='l',lat_1=5,lat_2=6,lat_0=52,lon_0=9)

    #m.drawcountries(linewidth=1.5)
    #m.drawcoastlines(linewidth=1.5)
    #m.drawstates()


    #m.bluemarble()

    m.etopo()

    plt.title("Geo Plotting Tutorial")
    plt.show()

    #plt.savefig('map.png')

# https://matplotlib.org/gallery/animation/dynamic_image2.html


# are you getting an error like:
# ImportError: The _imaging C module is not installed
# This meanss you have PIL, but you have the wrong bit version.
# If it says you don't have PIL at all, then you better go grab it
# but this should have come with your matplotlib installation.

coolerProjections()
