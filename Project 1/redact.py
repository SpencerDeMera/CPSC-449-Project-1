import sys
import http.client
import json
import urllib.parse
from urllib.request import urlopen
import http.server
import socketserver

PORT = 8080


def messageDecoder():
    FoaasAPI = 'foaas.com'  # foaas api address
    FoaasAPIpath = sys.argv[1]  # gets FOAAS path+name
    PurgoAPI = 'https://www.purgomalum.com/service'  # purgo api address

    # requesting JSON data
    connect1 = http.client.HTTPSConnection(FoaasAPI)
    header = {'Accept': 'application/json'}
    connect1.request('GET', FoaasAPIpath, headers=header)

    # Retreive FOAAS json data
    response1 = connect1.getresponse().read()
    jsonData1 = json.loads(response1.decode())

    # Encode and concat Purgo URL
    encoded = urllib.parse.quote(jsonData1['message'])  # encodes value for webAddress
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


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        FoaasAPI = 'foaas.com'  # foaas api address
        FoaasAPIpath = sys.argv[1]  # gets FOAAS path+name
        PurgoAPI = 'https://www.purgomalum.com/service'  # purgo api address

        # requesting JSON data
        connect1 = http.client.HTTPSConnection(FoaasAPI)
        header = {'Accept': 'application/json'}
        connect1.request('GET', FoaasAPIpath, headers=header)

        # Retreive FOAAS json data
        response1 = connect1.getresponse().read()
        jsonData1 = json.loads(response1.decode())

        # Encode and concat Purgo URL
        encoded = urllib.parse.quote(jsonData1['message'])  # encodes value for webAddress
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
        message = jsonData1['message']
        subtitle = jsonData1['subtitle']
        payload = (f'<!DOCTYPE html> <html> <head> <title>FOAAS - FUCK OFF, TOM. - EVERYONE</title> <meta charset="utf-8">'
                   f'<meta property="og:title" content="FUCK OFF, TOM. - EVERYONE"> <meta property="og:description" content="FUCK OFF, TOM. - EVERYONE"> <meta name="twitter:card" content="summary" /> <meta name="twitter:site" content="@foaas" /> <meta name="twitter:title" content="FOAAS: Fuck Off As A Service" /> <meta name="twitter:description" content="FUCK OFF, TOM. - EVERYONE" />  <meta name="viewport" content="width=device-width, initial-scale=1"> <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet"></head>'
                   f'<body style="margin-top:40px;"> <div class="container"> <div id="view-10"> <div class="hero-unit">'
                   f'<h1>{message}</h1>'
                   f'<p><em>{subtitle}</em></p> </div> </div>'
                   f'<p style="text-align: center"><a href="https://foaas.com">foaas.com</a></p> </div> </body> </html>' )

        self.wfile.write(payload.encode('utf-8'))


with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
