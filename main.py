from elastichostsapi import ElastichostsApi

import os
import sys

if __name__ == "__main__":
    user = os.environ.get('EHUSER')
    apikey = os.environ.get('EHAPIKEY')
    
    if (not user):
        print "Please set enviornment variable 'EHUSER'"
        sys.exit(1)
        
    if (not apikey):
        print "Please set enviornment variable 'EHAPIKEY'"
        sys.exit(1)

    ehconn = ElastichostsApi(user=user, 
                            apikey=apikey, 
                            json=True)
                            
    response = ehconn.execute("servers/list")
    print response.json()
