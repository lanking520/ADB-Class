import requests
import json



SearchAPI = "https://www.googleapis.com/customsearch/v1"
CustomEnginekey = '014170202143592210537:4zb34sjofuu'
JSONkey = 'AIzaSyBz-iFhhFx_sQSBMxKBMh9d5ZjD2nyQtLw'

query = "Columbia"


def googleQuery(query):
	payload = {'cx': CustomEnginekey , 'key': JSONkey ,'q' : query}
	r = requests.get(SearchAPI, params=payload)
	return json.loads(r.text)

print googleQuery(query)