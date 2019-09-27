import pandas
import random

from geo_coding import  get_geojson_data
from flask import Flask
import folium

from getting_data import get_data
from locations_of_assassinations_of_social_leaders import unique_dicts

app = Flask(__name__)

dep_name = 'department'
num_killings = 'assassinations'

import branca.colormap as cm
linear = cm.LinearColormap(
    ['green', 'yellow', 'red'],
    vmin=0, vmax=14
)

@app.route('/')
def index():
    m = folium.Map([3, -75], tiles='cartodbpositron', zoom_start=6)
    color_states(m)
    put_marks_on_map(m)
    return m._repr_html_()


def color_states(m):
    folium.GeoJson(
        geo_json_data,
        style_function=lambda feature: {
            'fillColor': linear(feature['properties'][num_killings]),
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5'
        },
        tooltip=folium.GeoJsonTooltip(fields=[dep_name, num_killings],
                                      style="font-family: san serif;",
                                      localize=True),

        highlight_function=lambda x: {'weight': 3, 'fillColor': 'blue'}
    ).add_to(m)


def put_marks_on_map(m):
    for datum in data:
        feats = [f for f in geo_json_municipios_data['features'] if is_in_state_and_city(datum, f)]
        if len(feats) == 0:
            print('could not locate: %s' % str(datum))
            continue
        uncertain_loc = [x + random.normalvariate(0, 0.01) for x in feats[0]['geometry']['coordinates']]
        location = tuple(reversed(uncertain_loc))  # TODO: WhyTF reversed!!?
        assert len(location) == 2
        pandas.set_option('display.max_colwidth', 1000)  # width in which unit??
        df = pandas.DataFrame(data=[{'key': k, 'value': v} for k, v in datum.items() if
                                    k in ['Nombre', 'Apellidos', 'Fecha', 'Perfil de liderazgo']])
        html = df.to_html(classes='table table-responsive table-hover table-striped table-condensed')  #
        popup = folium.Popup(html, max_width=400)  # width in which unit??

        folium.Marker(location,
                      tooltip='%s %s' % (datum['Nombre'], datum['Apellidos']),
                      popup=popup,
                      icon=folium.Icon(color="red", icon_color='red')
                      ).add_to(m)


def is_in_state_and_city(datum, feat):
    sd = feat['properties']['search_dict']
    return sd['state'] == datum['Departamento'] and sd['city'] == datum['Municipio']

if __name__ == '__main__':
    data = get_data()

    with open('colombia_departments.csv','r') as f:
        departments = [l.split('\t')[0] for l in f.readlines()]
    geo_searches = [{'country': 'Colombia', 'state':dep} for dep in departments]

    geo_json_data = get_geojson_data(geo_searches, polygon_geojson=1, geometry_type='Polygon',
                                     geojson_file='departments.json')

    geo_searches = [{'country':'Colombia','state':d['Departamento'],'city':d['Municipio']} for d in data]
    geo_searches = unique_dicts(geo_searches)
    geo_json_municipios_data = get_geojson_data(geo_searches=geo_searches, polygon_geojson=0, geometry_type='Point',
                                                geojson_file='municipios.json')

    for feat in geo_json_data['features']:
        feat['properties'][dep_name] = feat['properties']['geocoding']['name']
        feat['properties'][num_killings] = len([d for d in data if d['Departamento']==feat['properties']['geocoding']['name']])

    app.run(debug=True)
