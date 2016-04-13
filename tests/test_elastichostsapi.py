import unittest

from src.elastichostsapi import ElastichostsApi

class TestElastichostsApi(unittest.TestCase):
    def setUp(self):
        pass
        
    def testFormRequestCorrectUri(self):
        ehconn = ElastichostsApi(user="test", apikey="test")
        uri, headers = ehconn.formRequest("servers/list")
        self.assertEquals(uri, "https://api-lon-p.elastichosts.com/servers/list")
        
    def testFormRequestPlainTextHeader(self):
        ehconn = ElastichostsApi(user="test", apikey="test")
        uri, headers = ehconn.formRequest("servers/list")
        acceptheader = headers['Accept']
        self.assertEquals(acceptheader, 'text/plain')
        
    def testFormRequestJsonHeader(self):
        ehconn = ElastichostsApi(user="test", apikey="test", json=True)
        uri, headers = ehconn.formRequest("servers/list")
        acceptheader = headers['Accept']
        self.assertEquals(acceptheader, 'application/json')
        
if __name__ == "__main__":
    unittest.main()
