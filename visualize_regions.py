from geo_coding import  get_geojson_data
from flask import Flask
import folium
app = Flask(__name__)

dep_name = 'name'

@app.route('/')
def index():
    m = folium.Map([3, -75], tiles='cartodbpositron', zoom_start=6)
    folium.GeoJson(
        geo_json_data,
        style_function=lambda feature: {
            'fillColor': '#008000',
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5'
        },
        tooltip=folium.GeoJsonTooltip(fields=[dep_name],
                                      style="font-family: san serif;",
                                      localize=True),
        highlight_function=lambda x: {'weight': 3, 'fillColor': 'red'}
    ).add_to(m)

    return m._repr_html_()

if __name__ == '__main__':

    with open('colombia_departments.csv','r') as f:
        departments = [l.split('\t')[0] for l in f.readlines()]
    geo_searches = [{'country': 'Colombia', 'state':dep} for dep in departments]
    print('got %d regions'%len(geo_searches))

    geo_json_data = get_geojson_data(geo_searches,polygon_geojson=1,geometry_type='Polygon',jsonl='departments.json')

    for feat in geo_json_data['features']:
        feat['properties'][dep_name] = feat['properties']['geocoding']['name']

    app.run(debug=True)
