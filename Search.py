import requests
import json
import sys
import re

SearchAPI = "https://www.googleapis.com/customsearch/v1"
libraryPath = "./proj1-stop.txt"

class DataClean:

    def __init__(self, path):
        f = open(path)
        self.library = f.readlines()

    def clean(self, query):
        query = re.sub('[^a-zA-Z0-9]', ' ', query)
        return query

    def stopWordRemoval(self, text):
        text = [w for w in text if not w in self.library and not w.replace('.', '', 1).isdigit()]
        return text


def googleQuery(CSEKey, JsonAPIKey, precsion, query):
	payload = {'cx': CSEKey , 'key': JsonAPIKey ,'q' : query}
	r = requests.get(SearchAPI, params=payload)
	return json.loads(r.text)

def main():
    if len(sys.argv) < 4:
        sys.stdout.write('Usage : python '+ sys.argv[0] +' <JsonAPIKey> <CSEKey> <precision> <query>\n')
        sys.exit()
    JsonAPIKey = sys.argv[1]
    CSEKey = sys.argv[2]
    precision = float(sys.argv[3])
    query = ' '.join(sys.argv[4:])
    DC = DataClean(libraryPath)
    # googleQuery(CSEKey, JsonAPIKey, precision, query)
    sys.stdout.write(query)




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



