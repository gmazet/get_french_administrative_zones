import json
import glob
from sys import exit
from numpy import linspace
from shapely.geometry import shape, Point
# depending on your version, use: from shapely.geometry import shape, Point

jsonfile='./france-geojson/regions.geojson'
jsonfile='./france-geojson/cantons-version-simplifiee.geojson'
#jsonfile='./france-geojson/communes-version-simplifiee.geojson'
jsonfile='./france-geojson/communes.geojson'
regjsonfile='./france-geojson/regions-version-simplifiee.geojson'
depjsonfile='./france-geojson/departements-version-simplifiee.geojson'

# load GeoJSON file containing sectors
with open(regjsonfile) as f1:
    regjs = json.load(f1)

# load GeoJSON file containing sectors
with open(depjsonfile) as f2:
    depjs = json.load(f2)

print "json file is loaded"

# construct point based on lon/lat returned by geocoder
for lat in linspace(45.9,46.2,20):
    for lon in linspace(5.8,6.5):

        foundreg=0

        print (float(lon),float(lat))
        point=Point((lon),float(lat))

        # check each polygon to see if it contains the point
        for feature in regjs['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                regcode=feature['properties']['code']
                regname=feature['properties']['nom']
                #print regname," (",regcode,")"
                foundreg=1
                break

         # Can't find associated region. Exit
        if (foundreg==0):
            continue

        # check each polygon to see if it contains the point
        for feature in depjs['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                depcode=feature['properties']['code']
                depname=feature['properties']['nom']
                #print depname," (",depcode,")"
                break


        depdir="./france-geojson/departements/%02d-*" % int(depcode)
        mydepdir= glob.glob(depdir)[0]
        #print mydepdir
        arrondfile="%s/arrondissements-*-*.geojson" % mydepdir
        arrondjsonfile= glob.glob(arrondfile)[0]
        #print arrondjsonfile

        # load GeoJSON file containing sectors
        with open(arrondjsonfile) as f3:
            arrondjs = json.load(f3)

        foundarrond=0
        # check each polygon to see if it contains the point
        for feature in arrondjs['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                arrondcode=feature['properties']['code']
                arrondname=feature['properties']['nom']
                #print arrondname," (",arrondcode,")"
                foundarrond=1
                break

        communefile="%s/communes-*-*.geojson" % mydepdir
        communejsonfile= glob.glob(communefile)[0]

        # load GeoJSON file containing sectors
        with open(communejsonfile) as f4:
            comjs = json.load(f4)

        foundcommune=0
        # check each polygon to see if it contains the point
        for feature in comjs['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                communecode=feature['properties']['code']
                communename=feature['properties']['nom']
                #print communename," (",communecode,")"
                foundcommune=1
                break


        print regname,depname,arrondname, communename

