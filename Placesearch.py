import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_key = 'AIzaSyBjdjvMLuBJYh9wn7erROA-SkCQGsJXjNk'

#gives list of places_ids available
serviceurl_placesearch = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
#gives extra details of each place
#serviceurl_placedetails = 

#First use the Place Search(Text Search Request) to obtain the place_ID and then use the Place 
#Details to get the ratings and address for all listed. 

con = sqlite3.connect('placedetailsdb.sqlite')
curs = con.cursor()

curs.execute('DROP TABLE IF EXISTS PlaceSearch')
curs.execute('DROP TABLE IF EXISTS PlaceDetails')

curs.execute('''CREATE TABLE PlaceSearch(
             place_id TEXT,
             name TEXT,
             open_now TEXT,
             price_level INTEGER,
             rating FLOAT,
             address TEXT,
             lat FLOAT,
             lng FLOAT)''')

parameters = dict()
query = input('What are you searching for?')     
parameters['query'] = query

parameters['location'] = "22.303940,114.170372"

while True:
    radius = input('Enter radius of search in meters: ')
    try:
        radius = int(radius)
        parameters['radius'] = radius
        break
    except:
        print('Please enter number for radius')
        
while True:
    maxprice = input('Enter the maximum price level you are looking for(0 to 4): ')
    try:
        maxprice = int(maxprice)
        parameters['maxprice'] = maxprice
        break
    except:
        print('Valid inputs are 0,1,2,3,4')
parameters['key'] = API_key

url = serviceurl_placesearch + urllib.parse.urlencode(parameters, safe = ',')
output = urllib.request.urlopen(url,context = None)
jsondata = json.loads(output.read())

if jsondata['status'] == 'OK':
    for i in range(len(jsondata['results'])):
        try:
            place_id = jsondata['results'][i]['place_id']
        except:
            place_id = 'Not Available'
        try:
            name = jsondata['results'][i]['name']
        except:
            name = 'Not Available'
        try:
            open_now = jsondata['results'][i]['opening_hours']['open_now']
        except:
            open_now = 'Not Available'
        try:
            price_level = jsondata['results'][i]['price_level']
        except:
            price_level = 'Not Available'
        try:
            rating = jsondata['results'][i]['rating']
        except:
            rating = 'Not Available'
        try:
            address = jsondata['results'][i]['formatted_address']
        except:
            address = 'Not Available'
        try:
            lat = jsondata['results'][i]['geometry']['location']['lat']
            lng =  jsondata['results'][i]['geometry']['location']['lng']
        except:
            lat = 'Not Available'
            lng = 'Not Available'
            
        curs.execute('''INSERT INTO PlaceSearch
                     (place_id,name,open_now,price_level,rating,address,lat,lng)
                     VALUES (?,?,?,?,?,?,?,?)''',(place_id,name,open_now,price_level,rating,memoryview(address.encode()),lat,lng))
        
        con.commit()
else:
    print('Invalid JSON data')
    
    


    
    
