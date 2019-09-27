import json
import pandas
import random
from geo_coding import  get_geojson_data
from flask import Flask
import folium

from getting_data import get_data

app = Flask(__name__)

@app.route('/')
def index():
    m = folium.Map([3, -75], tiles='cartodbpositron', zoom_start=6)

    def is_in_state_and_city(datum,f):
        search_dict = f['properties']['search_dict']
        return search_dict['state'] == datum['Departamento'] and search_dict['city'] == datum['Municipio']

    for datum in data:
        feats = [f for f in geo_json_data['features'] if is_in_state_and_city(datum,f)]
        if len(feats)==0:
            print('could not locate: %s'%str(datum))
            continue
        uncertain_loc = [x+random.normalvariate(0,0.01) for x in feats[0]['geometry']['coordinates']]
        location = tuple(reversed(uncertain_loc))#TODO: WhyTF reversed!!?
        assert len(location)==2
        pandas.set_option('display.max_colwidth', 1000) # width in which unit??
        df = pandas.DataFrame(data=[{'key':k,'value':v} for k,v in datum.items() if k in ['Nombre','Apellidos','Fecha','Perfil de liderazgo']])
        html = df.to_html(classes='table table-responsive table-hover table-striped table-condensed')#
        popup = folium.Popup(html,max_width=400) # width in which unit??

        folium.Marker(location,
                      tooltip='%s %s'%(datum['Nombre'],datum['Apellidos']),
                      popup=popup,
                      icon=folium.Icon(color="red",icon_color='red')
                      ).add_to(m)

    return m._repr_html_()

def unique_dicts(dicts):
    return [json.loads(s) for s in set([json.dumps(r) for r in dicts])]

if __name__ == '__main__':
    data = get_data()
    geo_searches = [{'country':'Colombia','state':d['Departamento'],'city':d['Municipio']} for d in data]
    geo_searches = unique_dicts(geo_searches)
    geo_json_data = get_geojson_data(geo_searches, polygon_geojson=0, geometry_type='Point',
                                     geojson_file='municipios.json')
    app.run(debug=True)
