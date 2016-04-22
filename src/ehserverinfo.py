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
        
        # Create dict of drive with it's uuid as the key
        driveuuid_dict = {}
        for drive in driveslist:
            driveuuid_dict[drive['drive']] = drive['name']
        
        # Iterate over the server list, generating mount keys as necessary
        # and checking whether the uuid of that mount is in the driveuuid_dict
        for server in serverlist:
            server_drive_dict[server['name']] = []
            for key in self.generateMountKey():
                if key in server:
                    if server[key] in driveuuid_dict:
                        server_drive_dict[server['name']].append(driveuuid_dict[server[key]])
                        
        return server_drive_dict
                        
        
    def generateMountKey(self):
        # Check for IDE mounts
        for i in xrange(2):
            for j in xrange(2):
                yield "ide:{}:{}".format(i, j)
    
        # Check for VirtIO blocks
        for i in xrange(8):
            yield "block:{}".format(i)
            
        # Check for ATA mounts
        for i in xrange(1):
            for j in xrange(6):
                yield "ata:{}:{}".format(i, j)
                
        # Check for SCSI mounts
        for i in xrange(1):
            for j in xrange(7):
                yield "scsi:{}:{}".format(i, j)
               
            
        
