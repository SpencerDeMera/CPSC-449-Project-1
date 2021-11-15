import sys
import http.client
import json
import urllib.parse
from urllib.request import urlopen
import http.server
import socketserver

PORT = 8080

def terminalDisplay():
    FoaasAPI = 'foaas.com'                                      # foaas api web address
    FoaasAPIpath = sys.argv[1]                                  # gets FOAAS path+name
    PurgoAPI = 'https://www.purgomalum.com/service'             # purgo api web address

    # requesting JSON data
    connect1 = http.client.HTTPSConnection(FoaasAPI)            # applies HTTPS connection to FoaasAPI 
    header = {'Accept': 'application/json'}                     # header for https request to Accpet json as a response
    connect1.request('GET', FoaasAPIpath, headers=header)       # Requests /GET with given https connection & path/extension

    # Retreive FOAAS json data
    response1 = connect1.getresponse().read()                   # Reads JSON response from connect1
    jsonData1 = json.loads(response1.decode())                  # decodes and loads response1 into a python string dictionary 'jsonData1'

    # Encode and concat Purgo URL
    encoded = urllib.parse.quote(jsonData1['message'])          # encodes value for webAddress
    encodedURL = '/json?text=' + encoded                        # Concats encoded message to the purgoAPI /GET path
                                                                # EX => '/json?text=Why?%20Because%20Fuck%20You,%20that's%20why.'
    # Request and retreive censored FOAAS 'message'
    response2 = urlopen(PurgoAPI + encodedURL).read()           # Reads JSON respons from URL opened at 'https://www.purgomalum.com/service/json?text=Why?%20Because%20Fuck%20You,%20that's%20why.'
    jsonData2 = json.loads(response2)                           # decodes and loads response2 into a python string dictionary 'jsonData2'      

    # Swap censored 'message' into jsonData1
    jsonData1['message'] = jsonData2['result']                  # Replaces 'message' in jsonData1 with censored 'message' in jsonData2

    # print censored jsonData1 
    print(json.dumps(jsonData1, indent=4))

terminalDisplay()

print() # Adds spacing between terminal output and PORT display

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        FoaasAPI = 'foaas.com'                                      # foaas api web address
        FoaasAPIpath = self.path                                    # gets FOAAS path+name
        PurgoAPI = 'https://www.purgomalum.com/service'             # purgo api web address

        # requesting JSON data
        connect1 = http.client.HTTPSConnection(FoaasAPI)            # applies HTTPS connection to FoaasAPI 
        header = {'Accept': 'application/json'}                     # header for https request to Accpet json as a response
        connect1.request('GET', FoaasAPIpath, headers=header)       # Requests /GET with given https connection & path/extension

        # Retreive FOAAS json data
        response1 = connect1.getresponse().read()                   # Reads JSON response from connect1
        jsonData1 = json.loads(response1.decode())                  # decodes and loads response1 into a python string dictionary 'jsonData1'

        # Encode and concat Purgo URL
        encoded = urllib.parse.quote(jsonData1['message'])          # encodes value for webAddress
        encodedURL = '/json?text=' + encoded                        # Concats encoded message to the purgoAPI /GET path
                                                                    # EX => '/json?text=Why?%20Because%20Fuck%20You,%20that's%20why.'
        # Request and retreive censored FOAAS 'message'
        response2 = urlopen(PurgoAPI + encodedURL).read()           # Reads JSON respons from URL opened at 'https://www.purgomalum.com/service/json?text=Why?%20Because%20Fuck%20You,%20that's%20why.'
        jsonData2 = json.loads(response2)                           # decodes and loads response2 into a python string dictionary 'jsonData2'      

        # Swap censored 'message' into jsonData1
        jsonData1['message'] = jsonData2['result']                  # Replaces 'message' in jsonData1 with censored 'message' in jsonData2
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
