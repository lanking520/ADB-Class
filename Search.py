import requests
import json
import sys



SearchAPI = "https://www.googleapis.com/customsearch/v1"


def googleQuery(CSEKey, JsonAPIKey, precsion, query):
	payload = {'cx': CSEKey , 'key': JsonAPIKey ,'q' : query}
	r = requests.get(SearchAPI, params=payload)
	return json.loads(r.text)


def main():

    JsonAPIKey = sys.argv[1]
    CSEKey = sys.argv[2]
    precision = sys.argv[3]
    query = sys.argv[4]
    print(googleQuery(CSEKey, JsonAPIKey, precision, query))




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



