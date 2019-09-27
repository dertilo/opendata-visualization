import json
import os
import pandas
import camelot
import re

def read_jsonl(file):
    with open(file,'rb') as f:
        data = [json.loads(l.decode('utf-8')) for l in f]
    return data

def write_jsonl(file, data):
    with open(file, 'wb') as f:
        strings = (json.dumps(d, ensure_ascii=False) + '\n' for d in data)
        f.writelines((s.encode('utf-8') for s in strings))

def correct_table_parsing_errors(datum):
    county, city = datum['Departamento'],datum['Municipio']
    if not city.capitalize() == city:
        l = re.compile("[A-Z]").split(city)
        county_suffix = l[0]
        city = city[len(county_suffix):]
        county = county+county_suffix

    datum['Departamento'] = county.replace('\n','')
    datum['Municipio'] = city.replace('\n','')

def get_pdf_file(
        pdf_url,
    ):
    pdf_file = pdf_url.split('/')[-1]
    if not os.path.isfile(pdf_file):
        os.system('curl -OL %s' % pdf_url)
    return pdf_file

def parse_table_in_pdf(pdf_file):
    tables = camelot.read_pdf(pdf_file, pages='all', split_text=True)
    data = [row for table in tables for row in table.data[1:]]
    header = data.pop(0)
    data = [{k: v.replace('\n','') if isinstance(v,str) else v for k, v in zip(header, datum)} for datum in data]
    [correct_table_parsing_errors(c) for c in data]
    return data

def get_data(
        pdf_file=None,
        file='data.jsonl'):
    if not os.path.isfile(file):
        assert pdf_file is not None
        data = parse_table_in_pdf(pdf_file)
        write_jsonl(file, data)
    else:
        data = read_jsonl(file)
    return data

if __name__ == '__main__':
    pdf_url = 'https://www.queremosdatos.co/request/418/response/856/attach/6/Homicidios2017%202018FINAL.pdf'
    data = get_data(get_pdf_file(pdf_url=pdf_url),file='data_1.jsonl')
    df = pandas.DataFrame(data=data)
    print(df[['Municipio','Apellidos','Fecha']][:3])
