import sys
import http.client
import json
import urllib.parse
from urllib.request import urlopen

def messageDecoder():
    FoaasAPI = 'foaas.com' # foaas api address
    FoaasAPIpath = sys.argv[1] # gets FOAAS path+name
    PurgoAPI = 'https://www.purgomalum.com/service'

    # requesting JSON data
    connect1 = http.client.HTTPSConnection(FoaasAPI)
    header = {'Accept': 'application/json'}
    connect1.request('GET', FoaasAPIpath, headers=header)

    # Retreive FOAAS json data
    response1 = connect1.getresponse().read()
    jsonData1 = json.loads(response1.decode())

    # Encode and concat Purgo URL
    encoded = urllib.parse.quote(jsonData1['message']) # encodes value for webAddress
    encodedURL = '/json?text=' + encoded

    # DOES NOT work for some reason :/
    # connect2 = http.client.HTTPSConnection(PurgoAPI)
    # connect2.request('GET', encodedURL, headers=header)
    # response2 = connect2.getresponse().read()

    # Request and retreive censored FOAAS 'message'
    response2 = urlopen(PurgoAPI + encodedURL).read()
    jsonData2 = json.loads(response2)

    # Swap censored 'message' into jsonData1
    jsonData1['message'] = jsonData2['result']

    # print censored jsonData1 
    print(json.dumps(jsonData1, indent=4))

messageDecoder()