#!/usr/bin/python
from elasticsearch import Elasticsearch
from elasticsearch import *
import config as config

# app = Flask(__name__)

class DataPrep:
    def __init__(self,fileName):
        self.fileName = fileName
        self.es= Elasticsearch(config.ES_HOST)
        try:
            self.es.indices.create(index='cities', ignore=400)
            self.es.indices.create(index='country_code', ignore=400)
            mapping = {"city": { "properties": { "coordinates": { "type": "geo_point" }}}}
            self.es.indices.put_mapping(index='cities',doc_type='city',body=mapping)
            self.parseAndDump()
        except Exception as e:
            print "error"
            print e
            exit(-1)


    def parseAndDump(self):
        country_code_set = set()
        try:
            with open(self.fileName,'r') as f:
                for line in f:
                    data = line.split('\t')
                    cityid,name,lat,lng,country_code = data[0],data[2],data[4],data[5],data[8]
                    if not cityid or not name or not lat or not lng or not country_code:
                        continue
                    print cityid,name,lat,lng,country_code
                    country_code_set.add(country_code)
                    cityData = {
                        "name": name,
                        "coordinates": {
                           "lat": lat,
                           "lon": lng,
                        },
                        "country_code" : country_code
                    }
                    res = self.es.index(index="cities",doc_type='city', id=cityid, body=cityData)

                count = 0
                for country in country_code_set:
                # print country
                    countcodeData = {
                        "country_code" : country 
                        }
                    res = self.es.index(index="country_code",doc_type='country', id=count, body=countcodeData)
                    count+=1
        except Exception as e:
            print "error"
            print e

if __name__ == '__main__':
    obj = DataPrep(config.FILENAME)
