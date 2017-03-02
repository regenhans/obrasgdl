import pymongo
from pymongo import MongoClient
import re

client = MongoClient()
db = client['obrasgdl']

for year in range(2007,2018):

	collection = db['year'+str(year)]

	for empresa in collection.find():

		rfc = empresa['contratista_rfc']
		esmoral = re.match( '[a-zA-Z]{3}\d{6}\w{3}', rfc)
		esfisica = re.match('[a-zA-Z]{4}\d{6}\w{3}', rfc)

		if not esfisica and not esmoral:
			print(str(year)+' '+ empresa['contratista'] + ' no es persona fisica ni moral y recibe ' + str(empresa['presupuesto'])  + ' de ' + empresa['origen_de_recursos'] + ' rfc: ' + empresa['contratista_rfc'])

