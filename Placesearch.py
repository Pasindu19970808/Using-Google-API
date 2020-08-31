import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3
import webbrowser

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_key = 'AIzaSyBjdjvMLuBJYh9wn7erROA-SkCQGsJXjNk'

#gives list of places_ids available
serviceurl_placesearch = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
serviceurl_placedetails = 'https://maps.googleapis.com/maps/api/place/details/json?'
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

curs.execute('''CREATE TABLE PlaceDetails(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
             name TEXT,
             lat FLOAT(10,6),
             lng FLOAT(10,6))''')


parameters = dict()
query = input('What are you searching for?')     
parameters['query'] = query

parameters['location'] = "22.311680,114.168762"

try:
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
            
        print('hi')
    else:
        print('Invalid JSON data')
        
    curs.execute('''SELECT place_id,name FROM PlaceSearch''')
    rows = curs.fetchall()
    fhand = open('location.js','w',-1,'utf-8')
    fhand.write('myData = [\n')
    for row in rows:
        #curs.execute('''INSERT OR IGNORE INTO PlaceDetails (name) VALUES (?)''',(row[1],))
        
        parameters1 = dict()
        parameters1['place_id'] = row[0]
        parameters1['key'] = API_key
        url1 = serviceurl_placedetails + urllib.parse.urlencode(parameters1, safe = ',')
        output1 = urllib.request.urlopen(url1, context = None)
        jsondata1 = json.loads(output1.read())
        if jsondata1['status'] == 'OK':
            try:
                lat = jsondata1['result']['geometry']['location']['lat']
            except:
                lat = 'Not Available'
            try:   
                lng = jsondata1['result']['geometry']['location']['lng']
            except:
                lng = 'Not Available'
            curs.execute('''INSERT INTO PlaceDetails (name,lat,lng) VALUES (?,?,?)''',(row[1],lat,lng))
        fhand.write("['"+str(row[1])+"' ,"+str(lat)+','+str(lng)+'],\n')
    fhand.write('];\n')
    fhand.close()
        
    con.commit()   
    curs.close()
    
    site = 'where.html'
    webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(site)
    
except KeyboardInterrupt:
    print('Stopped by user')

    
    
