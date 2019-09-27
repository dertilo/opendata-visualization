import json
import os

import geopandas
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
    else:
        for feat in geo_json['features']:
            feat['properties']['search_dict'] = search
    return geo_json

def get_geojson_data(geo_searches, polygon_geojson=0, geometry_type='Point', geojson_file ='some_file.json'):

    def first_feat_of_type(feats):
        feats = [f for f in feats if geometry_type in f['geometry']['type']]
        return [feats[0]] if len(feats)>0 else []

    if not os.path.isfile(geojson_file):
        geo_json_data = [
            get_geo(search=search, polygon_geojson=polygon_geojson, format='geocodejson') for search in geo_searches]
        features = [f for geo in geo_json_data for f in first_feat_of_type(geo['features'])]
        geo_json_data = {'type': 'FeatureCollection', 'features': features}

        with open(geojson_file, 'wb') as f:
            f.write(json.dumps(geo_json_data,ensure_ascii=False).encode('utf-8'))

    geo_json_data = simplify_polygons_with_geopandas(geojson_file)

    return geo_json_data

def simplify_polygons_with_geopandas(geojson_file,tolerance = 0.001):
    gdf = geopandas.GeoDataFrame.from_file(geojson_file)
    gdf['geometry'] = gdf['geometry'].simplify(tolerance, preserve_topology=True)
    geo_json_data = json.loads(gdf.to_json())
    return geo_json_data
