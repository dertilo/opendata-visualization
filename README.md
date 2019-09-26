# Visualizing Data concerning Homocides of Social Leaders in Colombia
data taken from [https://www.queremosdatos.co/](https://www.queremosdatos.co/)  

see [request for number of killed sociel leaders](https://www.queremosdatos.co/request/numero_de_lideres_sociales_muert)

## 1. pdf parsing
parse [Homicidios2017 2018FINAL.pdf](https://www.queremosdatos.co/request/418/response/856/attach/6/Homicidios2017%202018FINAL.pdf) with [camelot](https://github.com/atlanhq/camelot.git) receive [data.jsonl](data.jsonl)

    a small subset of the table: 
        
          Municipio        Apellidos       Fecha
        0    Carepa  Cartagena Úsuga  10/01/2017
        1    Sonsón   Alzate Londoño  12/01/2017
        2    Jardín    Suárez Osorio  22/01/2017
        
## 2. visualize departments

[departments.csv](colombia_departments.csv) copy-pasted from [statoids](http://www.statoids.com/uco.html)

get department-borders (geo-coding) from [nominatim](https://nominatim.org/release-docs/develop/api/Search/) and visualize with [folium](https://github.com/python-visualization/folium.git)
![departments](images/departments.png)


## 3. mark locations of assassinations
geo-coding of cities via [nominatim](https://nominatim.org/release-docs/develop/api/Search/) geojsons are written to [municipios.json](municipios.json)
each assassination gets a marker with pop containing information from [Homicidios2017 2018FINAL.pdf](https://www.queremosdatos.co/request/418/response/856/attach/6/Homicidios2017%202018FINAL.pdf)
![assassinations](images/killed_social_leaders.png)
