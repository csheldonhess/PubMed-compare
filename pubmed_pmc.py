from lxml import etree
from datetime import date, timedelta
import re
import requests
import time


NAMESPACES = {'ns0': 'http://www.openarchives.org/OAI/2.0/',
              'pmc': 'http://dtd.nlm.nih.gov/2.0/xsd/archivearticle'}

titles = []
start_date = date.today() - timedelta(3)
base_url = 'http://www.pubmedcentral.nih.gov/oai/oai.cgi?verb=ListRecords' 
oai_pmc_request = base_url + '&metadataPrefix=pmc&from={}'.format(str(start_date)) 
print(oai_pmc_request)
data = requests.get(oai_pmc_request)
doc = etree.XML(data.content)
records = doc.xpath('//ns0:record', namespaces=NAMESPACES)
for record in records:
    r = record.xpath(".//pmc:title-group/pmc:article-title", namespaces=NAMESPACES)
    if len(r) > 1:
        raise Exception('more than one title')
    record_string = etree.tostring(r[0])
    titles.append(re.sub(r'\<.*?\>', '', record_string).strip())


with open('pubmedPMC.txt', 'w') as f:
    for title in titles:
        f.write(title + '\n')
    