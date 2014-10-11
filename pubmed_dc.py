from lxml import etree
from datetime import date, timedelta
import requests
import re
import time

NAMESPACES = {'dc': 'http://purl.org/dc/elements/1.1/', 
            'oai_dc': 'http://www.openarchives.org/OAI/2.0/',
            'ns0': 'http://www.openarchives.org/OAI/2.0/',
            'arch': 'http://dtd.nlm.nih.gov/2.0/xsd/archivearticle'}

# def get_titles(doc):
#     titles = doc.xpath('//dc:title', namespaces=NAMESPACES)
#     titlelist = []
#     for title in titles:
#         if isinstance(title, etree._Element):
#             title = title.text
#         title = title.strip()
#         titlelist.append(title)
#     return titlelist

title_list = []
start_date = date.today() - timedelta(3)
base_url = 'http://www.pubmedcentral.nih.gov/oai/oai.cgi?verb=ListRecords' 
oai_dc_request = base_url + '&metadataPrefix=oai_dc&from={}'.format(str(start_date)) 
print(oai_dc_request)
data = requests.get(oai_dc_request)
doc = etree.XML(data.content)
titles = doc.xpath('//dc:title', namespaces=NAMESPACES)
for title in titles:
    if isinstance(title, etree._Element):
        title_string = etree.tostring(title)
    else:
        title_string = title
    title_list.append(re.sub(r'\<.*?\>', '', title_string).strip())

with open('pubmedDC.txt', 'w') as f:
    for title in title_list:
        title = title.encode('utf-8')
        f.write(title + '\n')
    