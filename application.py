#!/usr/bin/python
import os
from datetime import datetime
import json
from elasticsearch import Elasticsearch
from elasticsearch import *
from flask import Flask, request, Response, render_template
import config as config
try:
    es= Elasticsearch(config.ES_HOST)
except Exception as e:
    print "error"
    print e
    exit(-1)
 
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/cities/proximity")
def closestCities():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    k = request.args.get('size')
    country_code = request.args.get('country_code')
    if not country_code:
        country_code = 'ANYWHERE'
    queryBody = {
    	"sort" : [{
          	"_geo_distance" : {
              	"coordinates" : {
                    "lat" : lat,
                    "lon" : lon
              	}, 
              	"order" : "asc",
              	"unit" : "km"
          	}
      	}],
    	"query": {
    	    "bool" : {
        		"must" : {
        		},
                "filter" : {
            		"geo_distance" : {
                		"distance" : "10000km",
                		"coordinates" : {
                    		"lat" : lat,
                    		"lon" : lon
                		}
            		}
        		}
    		}
    	}
    }
    if country_code != 'ANYWHERE':
        queryBody['query']['bool']['must']['match'] = {'country_code' : country_code}
    else:
        queryBody['query']['bool']['must']['match_all'] = {}

    try:
        res = es.search(index = 'cities', scroll = '1s', body = queryBody, size = k)
    except Exception as e:
        print "error"
        return Response(json.dumps({"error":"something went wrong"}),content_type = 'application/json', status = 500)
    scroll_size=res["hits"]["total"]
    print scroll_size
    cityList = res["hits"]["hits"]

    k = min(k,len(cityList))
    print k
    output = set()
    for i in range(k):
        output.add(cityList[i]['_source']['name'])
    return Response(json.dumps(list(output)), content_type='application/json')

@app.route("/cities/lexical")
def citiesByName():
    keyword = request.args.get('keyword')
    keywords = keyword.split()
    queryBody = {
        "query": {
            "bool": {
                "should": []
            }
        }
    }
    for i in range(len(keywords)):
        queryBody['query']['bool']['should'].append({"wildcard": {"name": "*" + keywords[i] + "*" }})
    try:
        res = es.search(index = 'cities', scroll = '1s', body = queryBody)
    except Exception as e:
        print "error"
        print e
        return Response(json.dumps({"error":"something went wrong"}),content_type = 'application/json', status = 500)
    scroll_size=res["hits"]["total"]
    print scroll_size
    cityList = res["hits"]["hits"]
    count = 0
    output = set()
    while count<scroll_size:
            k = len(cityList)
            for j in range(k):
                output.add(cityList[j]['_source']['name'])
            count+=k
            scroll_id=res['_scroll_id']
            rs=es.scroll(scroll_id=scroll_id,scroll='1s')
            cityList = rs['hits']['hits']
    return Response(json.dumps(list(output)), content_type='application/json')

@app.route("/countries")
def allCountries():
    queryBody = {
        "query": {
                "bool": {
                    "must": {
                        "match_all" : {}
                    }
                }
        }
    }
    try:
        res = es.search(index = 'country_code', scroll = '1s', body = queryBody)
    except Exception as e:
        print "error"
        print e
        return Response(json.dumps({"error":"something went wrong"}),content_type = 'application/json', status = 500)
    scroll_size=res["hits"]["total"]
    print scroll_size
    countryCodeList = res["hits"]["hits"]
    count = 0
    output = set()
    while count<scroll_size:
            k = len(countryCodeList)
            for j in range(k):
                output.add(countryCodeList[j]['_source']['country_code'])
            count+=k
            scroll_id=res['_scroll_id']
            rs=es.scroll(scroll_id=scroll_id,scroll='1s')
            countryCodeList = rs['hits']['hits']
    return Response(json.dumps(list(output)), content_type='application/json')


if __name__ == "__main__":
    app.run(debug=True,threaded=True)


