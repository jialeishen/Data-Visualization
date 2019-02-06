# -*- coding: utf-8 -*-

########################
#Country Mapping
#Author: Jialei Shen
#E-mail: jshen20@syr.edu
#Latest: Feb 6, 2019
########################

import matplotlib.pyplot as plt
import geopandas as gpd
from descartes import PolygonPatch
from shapely.geometry import Polygon

######################################################

####INPUT PARAMETERS####
#Input the country names into this array.
countries = ['Pakistan', 'Qatar','Afghanistan','Bangladesh','Egypt','United Arab Emirates', 'Mongolia','India','Nepal','Ghana','Jordan','China','Senegal','Turkey','Bulgaria','Peru','Serbia','Iran']
#Input the value for each country into this array (following the order of country names).
values = [115.7, 92.4, 86, 83.3, 73, 64, 61.8, 60.6, 50, 49, 48, 41.4, 40, 39.1, 38.6, 38, 35.8, 34.2]
#Choose your projection method.
projMethod = 'World Robinson' #Normal; Mercator; World Robinson; Pseudo-Mercator;
#Choose the mapping color
legendColor = 'red' #orange; red; green; black; blue; grey;
#Set map title
mapTitle = "The world's most polluted countries"

######################################################

legendMin, legendMax = 0.2, 1.0 #alpha, from 0 to 1

legendColors = {
    'orange':'#F0A14C',
    'red':'#B22222',
    'green':'#008080',
    'black':'#000000',
    'blue':'#1F4C91',
    'grey':'#464646'
    }

#Map projection options
projMethods = {
    'Normal':'epsg:4326',
    'Mercator':'epsg:3395',
    'World Robinson': 'ESRI:54030',
    'Pseudo-Mercator': 'epsg:3857'
    } #please add more projection options

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


def plotCountryPatch( axes, country_name, fcolor , a):    
    # plot a country on the provided axes
    try:
        nami = world[world.name == country_name]
        nami2 = nami.to_crs({'init': projMethods[projMethod], 'no_defs': True})
        namigm = nami2.__geo_interface__['features']  # geopandas's geo_interface
        namig0 = {'type': namigm[0]['geometry']['type'], \
                  'coordinates': namigm[0]['geometry']['coordinates']}
        axes.add_patch(PolygonPatch( namig0, fc=fcolor, linewidth = 0.1, edgecolor='black', alpha=a))
    except:
        print('#############################################\nError [Name Error]: There is no '+country_name+' in the world, please check the country name.\n#############################################')


def value2alpha(vs):
    a = []
    vmax = max(vs)
    vmin = min(vs)
    for v in vs:
        a.append(float(legendMin+((legendMax-legendMin)*(v - vmin)/(vmax-vmin))))
    return a


def main():   
    print('''########################
#Country Mapping
#Author: Jialei Shen
#E-mail: jshen20@syr.edu
#Latest: Feb 5, 2019
########################\nRunning...''')
    
    if len(countries) > len(values):
        print('#############################################\nError [Range Error]: The country number is more than the value number.\n#############################################')
    elif len(countries) < len(values):
        print('#############################################\nError [Range Error]: The country number is less than the value number.\n#############################################')
    
    ax = world[(world.name != "Antarctica") & (world.name != "Fr. S. Antarctic Lands")].to_crs({'init': projMethods[projMethod], 'no_defs': True}).plot(
        color='white', linewidth = 0.1, edgecolor='black', figsize=(10.,5.))

    al = []
    al = value2alpha(values)
    for n in range(len(al)):
        plotCountryPatch(ax, countries[n], legendColors[legendColor], al[n])

    print('Drawing...')

    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.axis('off')
    ax.set_title(mapTitle)
    #ax2.axis('scaled')
    plt.show()
    print('Done!')


if __name__ == "__main__":
    main()
