import json
import os

import requests

def get_geo(search,**kwargs):
    # see: https://nominatim.org/release-docs/develop/api/Search/
    geocode_url = 'https://nominatim.openstreetmap.org/search'
    get_request = lambda params: json.loads(requests.get(geocode_url,params=params).text)
    geo_json = get_request({**search,**kwargs})

    if len(geo_json['features'])==0:
        search_string = '%2C'.join([s.replace(' ','+') for s in search.values()])
        geo_json = get_request({**{'q':search_string},**kwargs})

    if len(geo_json['features'])==0:
        print('could not find: %s'%str(search))
    return geo_json

def get_geojson_data(geo_searches, jsonl ='some_file.json'):

    if not os.path.isfile(jsonl):
        geo_json_data = [
            get_geo(search=search, polygon_geojson=1, format='geocodejson') for search in geo_searches]
        features = [f for geo in geo_json_data for k,f in enumerate(geo['features']) if k==0]
        geo_json_data = {'type': 'FeatureCollection', 'features': features}

        with open(jsonl, 'wb') as f:
            f.write(json.dumps(geo_json_data,ensure_ascii=False).encode('utf-8'))
    else:
        with open(jsonl, 'rb') as f:
            geo_json_data = json.loads(f.read().decode('utf-8'))

    return geo_json_data
