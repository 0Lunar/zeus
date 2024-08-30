import nmap as nm
import logging


class NetworkScan:
    def __init__(self, host: str = "127.0.0.1"):
        self.host = host
        self.nmap = nm.PortScanner()
        self.scanned = False
        self.scan = {}


    def portScan(self, port: str) -> dict:
        """ Scans a specific port on the host """

        try:
            scan = self.nmap.scan(self.host, port)
            self.scan = scan
            self.scanned = True

            return scan
        
        except Exception as e:
            logging.error(e)
            return {}


    def standardScan(self) -> dict:
        """ Performs a standard scan of the host """

        try:
            scan = self.nmap.scan(self.host)
            self.scan.update(scan)
            self.scanned = True

            return scan
        
        except Exception as e:
            logging.error(e)
            return {}

    def advancedScan(self, OSdetection: bool = True, hostDetection: bool = True, firewallEvasion: bool = False, ports: str = "") -> dict:
        """ Performs an advanced scan with customizable options """

        try:
            args = "-sC -sV "
            if hostDetection == False:
                args += "-Pn "

            if OSdetection:
                args += "-O "

            if firewallEvasion:
                args += "-sN "

            if ports != "":
                args += " -p " + ports
            
            scan = self.nmap.scan(self.host, arguments=args.strip())
            self.scan.update(scan)
            self.scanned = True

            return scan
        
        except Exception as e:
            logging.error(e)
            return {}
        

    def fastScan(self) -> dict:
        """ Performs a fast scan of the host """

        try:
            scan = self.nmap.scan(self.host, arguments="-F")
            self.scan.update(scan)
            self.scanned = True

            return scan
        
        except Exception as e:
            logging.error(e)
            return {}
    

    def all_hostsnames(self) -> list:
        """ Show all the hostnames """

        if self.scanned:
            try:
                hostnames = []

                for i in self.scan['scan']:
                    if self.scan['scan'][i]['hostnames'][0]['name'] != '':
                        hostnames.append(self.scan['scan'][i]['hostnames'][0]['name'])
                    else:
                        hostnames.append("Unknown")

                return hostnames

            except Exception as e:
                logging.error(e)
                return {}
        

    def all_hosts(self) -> dict:
        """ Show all hosts """

        if self.scanned:
            try:
                hosts = {}

                for i in self.scan['scan']:

                    hostname = self.scan['scan'][i]['hostnames'][0]['name']

                    if hostname == "":
                        hostname = "Unknown"

                    host = {i: hostname}
                    hosts.update(host)

                return hosts

            except Exception as e:
                logging.error(e)
                return {}

    
    def ports(self, hostip: str) -> dict:
        """ Show detected ports on a single host """

        if self.scanned:
            try:
                ports = {}

                if "tcp" in self.scan['scan'][hostip]:
                    for i in self.scan['scan'][hostip]['tcp']:
                        portInfo = self.scan['scan'][hostip]['tcp'][i]

                        ports.update({i: {"status": portInfo['state'], "name": portInfo['name']}})

                return ports

            except Exception as e:
                logging.error(e)
                return {}
    
    def clean(self):
        self.scan = {}
        self.scanned = False