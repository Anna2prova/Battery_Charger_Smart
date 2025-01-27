import json
import random
import time
import cherrypy
import requests

class CheckUpdate():

    def __init__(self,url):
        self.url=url
        response= requests.get(self.url)
        self.response_json_alldevices = response.json()
        self.NumberofDevice=len(self.response_json_alldevices)
        self.devdel=[]

    def makerequest(self):
        for i in range(self.NumberofDevice):
            output=self.response_json_alldevices
            print(f'actual time {time.time()}')
            lastUpDate=int(self.response_json_alldevices[i]['lastUpDate'])
            print(f'actual time {lastUpDate}')
            dif=int(time.time()-lastUpDate)
            print({dif})
            if dif>120:
                print(self.response_json_alldevices[i])
                self.devdel.append(i)
        print(self.devdel)
        self.devdel.reverse()
        print(self.devdel)
        print(output)
        for i in range(len(self.devdel)):
            output.pop(self.devdel[i])
        print(output)

        # aggiornare il catalogo 
        response= requests.get('http://127.0.0.1:8080/catalog')
        catalog = response.json()
        catalog['DeviceList']=output
        json.dump(catalog, open('setting.json', 'w'), indent=2)
        # json.dump(catalog, open('Catalog.json', 'w'), indent=2)

if __name__ == '__main__':
    while True:
        Catalog=json.load(open('Catalog.json'))
        URL=Catalog['Catalog_url']+'/AllDevices'
        daily=CheckUpdate(URL)
        daily.makerequest()
        time.sleep(60)
