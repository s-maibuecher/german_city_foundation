from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np



def coolerProjections():
    m = Basemap(projection='mill',llcrnrlat=47.1,urcrnrlat=55.2, llcrnrlon=5.5,urcrnrlon=15.3, resolution='l')

    m.drawcountries()
    m.drawstates()


    m.bluemarble()

    plt.title("Geo Plotting Tutorial")
    plt.show()

    #plt.savefig('map.png')


# are you getting an error like:
# ImportError: The _imaging C module is not installed
# This meanss you have PIL, but you have the wrong bit version.
# If it says you don't have PIL at all, then you better go grab it
# but this should have come with your matplotlib installation.

coolerProjections()
