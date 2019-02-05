# -*- coding: utf-8 -*-

########################
#Author: Jialei Shen
#E-mail: jshen20@syr.edu
#Latest: Feb 5, 2019
########################

import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt
import csv
from array import *
from cartopy import crs as ccrs

#Map projection options
projMethods = {
    'Normal':'epsg:4326',
    'Mercator':'epsg:3395',
    'World Robinson': 'ESRI:54030',
    'Pseudo-Mercator': 'epsg:3857'
    } #please add more projection options

####################################################################

####INPUT PARAMETERS####
#Input the city names into this array. 
cities = ['nanjing','beijing','tokyo','new york','toronto','sydney','madrid', 'atlanta', 'delhi', 'paris', 'seattle', 'lublin', 'cairo']
#Input the value for each city into this array (following the order of city names).
values = [5,1,3,7,5,3,2,8,2,1,4,6,9]
#Choose your projection method.
projMethod = 'World Robinson'

####################################################################


def cityDatabase():
    csvDataFrame = []
    csvCities = []
    csvCounts = []
    csvLats = []
    csvLngs = []
    with open('worldcities.csv') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            cityName = row[0].lower()
            count = row[1].lower()
            lat = float(row[2])
            lng = float(row[3])
            csvCities.append(cityName)
            csvCounts.append(count)
            csvLats.append(lat)
            csvLngs.append(lng)
        csvDataFrame = [csvCities,csvCounts,csvLats,csvLngs]
    return csvDataFrame


def cityDuplicate(seq,item):
    start_at = -1
    locs = []
    counts = []
    lats = []
    lngs = []
    while True:
        try:
            loc = seq[0].index(item,start_at+1)
        except ValueError:
            break
        else:
            counts.append(seq[1][loc])
            lats.append(seq[2][loc])
            lngs.append(seq[3][loc])
            locs.append(loc)
            start_at = loc
    return locs,counts,lats,lngs


def cityCoor(cs):
    try:
        cityIndices = []
        cityCounts = []
        cityLats = []
        cityLngs = []
        citySets = []
        counts = []
        lats = []
        lngs = []
        cb = cityDatabase()
        for c in cs:
            c = c.lower()
            cityIndices,cityCounts,cityLats,cityLngs = cityDuplicate(cb,c)
            citySets = [cityIndices,cityCounts,cityLats,cityLngs]
            #print(citySets)
            if len(cityIndices) == 1:
                ci = cityIndices[0]
                counts.append(cb[1][ci])
                lats.append(cb[2][ci])
                lngs.append(cb[3][ci])
            elif len(cityIndices) == 0:
                break
            else:
                print('----------------------------------------------\nThe city '+c+' is located in: ')
                m = len(citySets[0])
                for n in range(m):
                    print(str(n)+': '+citySets[1][n]+' (lat: '+str(citySets[2][n])+'; lng: '+str(citySets[3][n])+')')
                index = int(input('----------------------------------------------\nChoose city INDEX: '))
                counts.append(citySets[1][index])
                lats.append(citySets[2][index])
                lngs.append(citySets[3][index])            
        return counts,lats,lngs
    except:
        print('#############################################\nError [Name Error]: \nThe cities you input are not in the database.\nPlease check the city names.\n#############################################')


def circleSize(vs):
    newValues = []
    for v in vs:
        newValues.append(float(100.+(v-min(vs))*900./(max(vs)-min(vs))))
    return newValues


def main():
    print('''########################
#Mapping Plots
#Author: Jialei Shen
#E-mail: jshen20@syr.edu
#Latest: Feb 5, 2019
########################\nRunning...''')
    counts,lats,lngs = cityCoor(cities)
    df = pd.DataFrame(
        {'City': cities,
         'Country': counts,
         'Latitude': lats,
         'Longitude': lngs
            })
    df['Coordinates'] = list(zip(df.Longitude, df.Latitude))
    df['Coordinates'] = df['Coordinates'].apply(Point)
    gdf = geopandas.GeoDataFrame(df, geometry='Coordinates')

    gdfProj = gdf.copy()
    #print the coordinates before projected
    print('\n+++++++++++++++++++++++++\nCity List:')
    print(gdfProj['City'])
    print('+++++++++++++++++++++++++\n')
    gdfCrs = gdfProj['Coordinates']
    gdfCrs.crs = {'init': 'epsg:4326', 'no_defs': True}
    
    gdfCrs = gdfCrs.to_crs({'init': projMethods[projMethod]})
    #print the coordinates after projected
    print('Mapping...')

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world = world.to_crs({'init': projMethods[projMethod]})

    #inside [..], choose the countries/continents you want and/or don't want to be shown in the map
    #use world.name == '..'; world.continent == '..'; world.name != '..'; world.continent != '..';...
    ax = world[(world.name != "Antarctica") & (world.name != "Fr. S. Antarctic Lands")].plot(
    color='#E7EEF1', linewidth = 0.1, edgecolor='black', figsize=(10.,5.))

    gdfCrs.plot(ax=ax, alpha=0.5, linewidth = 0.5, edgecolor='black', color='#F0A14C',markersize = circleSize(values))
    #show axis? ('off'/'on')
    ax.axis('off')
    plt.show()
    print('Done!')
    

if __name__ == "__main__":
    main()