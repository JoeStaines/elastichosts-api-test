class EHServerInfo():
    def __init__(self, ehconn):
        self.ehconn = ehconn
        
    def printServersAndDrives(self):
        # Get dict of {servername: [drives]}
        server_drive_map = self.getServersInfo()
        
        # Pretty print server and drivesp
        for server, drives in server_drive_map.iteritems():
            drives_str = ' '.join(drives)
            print "{}: {}".format(server, drives_str)
        
    def getServersInfo(self):
        # Retrieve list of servers and drives
        serverlist = self.ehconn.execute('servers/info').json()
        driveslist = self.ehconn.execute('drives/info').json()
        
        return self.mapServersToDrives(serverlist, driveslist)
            
    def mapServersToDrives(self, serverlist, driveslist):
        # dict that contains the mapping between servers and drives
        server_drive_dict = {}
        
        # Iterate once over the servers toadd them to do dict
        for server in serverlist:
            server_drive_dict[server['name']] = []
        
        # Get info on each server
        for drive in driveslist:
            # boolean to check if we have found the drive/server mapping
            # and use to stop checking more servers
            found = False
            
            for server in serverlist:
                # Check each drive number in the server json
                # to see if it matches the drive uuid
                for i in range(8):
                    key = "block:{}".format(i)
                    if key in server:
                        if server[key] == drive['drive']:
                            servername = server['name']
                            server_drive_dict[servername].append(drive['name'])
                            found = True
                            break
                if found:
                    break
                
        return server_drive_dict
            
        
