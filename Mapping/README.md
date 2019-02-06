# Mapping

## Functions
Mapping data on a map
 - [City Mapping](https://github.com/jialeishen/Data-Visualization/blob/master/Mapping/citymapping.py): Mapping data to cities;
 - [Country Mapping](https://github.com/jialeishen/Data-Visualization/blob/master/Mapping/countrymapping.py): Mapping data to countries

## Dependencies
 - [pandas](https://pandas.pydata.org/)
 - [geopandas](http://geopandas.org/)
 - [matplotlib](https://matplotlib.org/)

## How to use
 - Input city/country names: `cities = ['tokyo','moscow','shanghai','beijing','seoul','new york','new delhi','guangzhou','mexico city','hong kong']` -> the city names are NOT case-sensitive.
 - Input city/country values: `values = [3463,2369,2044,1988,1885,1806,1789,1730,1678,1600]` -> the values will be auto-scaled.
 - Choose map projection: `projMethod = 'World Robinson'` 
 - Choose mapping color: `legendColor = 'red'`
 - Set map title: `mapTitle = '10 busiest metros in the world'`
 - Done!

![city](cityimage.png)
![country](countryimage.png)


