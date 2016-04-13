from src.ehserverinfo import EHServerInfo
from src.elastichostsapi import ElastichostsApi

import unittest

class TestEHServerInfo(unittest.TestCase):
    def setUp(self):
        self.ehconn = ElastichostsApi("user", "key")
        self.ehinfo = EHServerInfo(self.ehconn)
        
    def testOneServerToOneDrive(self):
        serverlist = [{  'name': 'server1',
                        'block:0': 'uuid1'  }]
        driveslist = [{  'name': 'drive1',
                        'drive': 'uuid1'    }]
                        
        server_map = self.ehinfo.mapServersToDrives(serverlist, driveslist)
        test_map = { 'server1': ['drive1'] }
        
        self.assertDictEqual(server_map, test_map)
        
    def testOneServerToOneDriveNoMatch(self):
        serverlist = [{  'name': 'server1',
                        'block:0': 'uuid1'  }]
        driveslist = [{  'name': 'drive1',
                        'drive': 'uuid2'    }]
                        
        server_map = self.ehinfo.mapServersToDrives(serverlist, driveslist)
        test_map = { 'server1': [] }
        
        self.assertDictEqual(server_map, test_map)
        
    def testOneServerToTwoDrives(self):
        serverlist = [{ 'name': 'server1',
                        'block:0': 'uuid1',
                        'block:1': 'uuid2'  }]
        driveslist = [{ 'name': 'drive1',
                        'drive': 'uuid1'    },
                      { 'name': 'drive2',
                        'drive': 'uuid2'    }]
                        
        server_map = self.ehinfo.mapServersToDrives(serverlist, driveslist)
        test_map = { 'server1': ['drive1', 'drive2'] }
        
        self.assertDictEqual(server_map, test_map)
        
    def testTwoServerToTwoDrives(self):
        serverlist = [{ 'name': 'server1',
                        'block:0': 'uuid1', },
                      { 'name': 'server2',
                        'block:0': 'uuid2'  }]
                        
        driveslist = [{ 'name': 'drive1',
                        'drive': 'uuid1'    },
                      { 'name': 'drive2',
                        'drive': 'uuid2'    }]
                        
        server_map = self.ehinfo.mapServersToDrives(serverlist, driveslist)
        test_map = { 'server1': ['drive1'], 'server2': ['drive2'] }
        
        self.assertDictEqual(server_map, test_map)
