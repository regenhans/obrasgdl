import urllib
import csv
from bs4 import BeautifulSoup
from urllib import request, error, parse
import pymongo
from pymongo import MongoClient
import re

# DB
client = MongoClient()
db = client['obrasgdl']

url = "http://enlinea.guadalajara.gob.mx:8800/obras/obraspublicas/listadoObras.php?year="

count = 0 
for year in range(2007,2018):
	print(count)
	# Create http request
	request = urllib.request.Request(url + str(year))
	request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
	html = urllib.request.urlopen(request)
	soup = BeautifulSoup(html ,  "html.parser")

	rows = soup.find(id="tableWeb").find("tbody").find_all("tr",recursive=False)
	
	##mongo and csv 
	year_collection = db['year'+str(year)]



	with open('./csv/year'+str(year)+'.csv', 'w+') as csvfile:
		fieldnames = ['contrato', 'estatus', 'mes', 'modalidad', 'origen_de_recursos', 'tipo_infraestructura','descripcion_obra', 'ubicacion','zona','presupuesto','ejercido_url', 'contratista', 'contratista_rfc']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()


		for row in rows:
			data = {}
			cells = row.find_all("td",recursive=False)
			data['contrato'] = str(cells[0].get_text()).strip()
			data['estatus'] = str(cells[1].get_text()).strip()
			data['mes'] = str(cells[2].get_text()).strip()
			data['modalidad'] =  str(cells[3].get_text()).strip()
			data['origen_de_recursos'] = str(cells[4].get_text()).strip()
			data['tipo_infraestructura'] = str(cells[5].get_text()).strip()
			data['descripcion_obra'] = str(cells[6].get_text()).strip()
			data['ubicacion'] = str(cells[7].get_text()).strip()
			data['zona'] = str(cells[8].get_text()).strip()
			presupuesto = cells[9].get_text().strip()
			price = re.sub('[$,]', '', presupuesto)
			data['presupuesto'] = float(price)
			data['ejercido_url'] = str(cells[10].find('a')['href']).strip()
			data['contratista'] = str(cells[11].get_text()).strip()
			rfc = cells[12].get_text().strip()
			cleanRFC = re.sub('[ /-]', '', rfc)
			data['contratista_rfc'] = str(cleanRFC)

			#write on csv
			writer.writerow(data)
			#write on DB
			year_collection.insert(data)








		