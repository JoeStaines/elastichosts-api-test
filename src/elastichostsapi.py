import requests

class ElastichostsApi():
    def __init__(self, user, apikey, uri="https://api-lon-p.elastichosts.com/", json=False):
        self.user = user
        self.apikey = apikey
        self.uri = uri
        self.json = json
        
    def execute(self, command):
        # Build a uri string to send a request to ElectricHosts api
        fulluri, headers = self.formRequest(command)
        return requests.get(fulluri, headers=headers, auth=(self.user, self.apikey))
        
    def formRequest(self, command):
        # Constuct headers to retrieve json  from api (if json is turned on)
        jsonval = "application/json" if self.json else "text/plain"
        headers = {
            "Content-Type": "text/plain", 
            "Accept": jsonval   
        }
        
        fulluri = self.uri + command
        return (fulluri, headers)
