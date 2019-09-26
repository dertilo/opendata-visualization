import json
import os
import camelot
import re

def read_jsonl(file):
    with open(file,'r') as f:
        data = [json.loads(l) for l in f]
    return data

def write_jsonl(file, data):
    with open(file, 'w') as f:
        f.writelines([json.dumps(d) + '\n' for d in data])

def corret_table_parsing_erros(datum):
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
    data = [{k: v for k, v in zip(header, datum)} for datum in data]
    [corret_table_parsing_erros(c) for c in data]
    return data

def get_data(
        pdf_file,
        file='data.jsonl'):
    if not os.path.isfile(file):
        data = parse_table_in_pdf(pdf_file)
        write_jsonl(file, data)
    else:
        data = read_jsonl(file)
    return data

if __name__ == '__main__':
    pdf_url = 'https://www.queremosdatos.co/request/418/response/856/attach/6/Homicidios2017%202018FINAL.pdf'
    data = get_data(get_pdf_file(pdf_url=pdf_url))
