import os
import re

from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import Scope


class Finder:
    def fetch_devices(self):
        wsd = WSDiscovery()
        scope1 = Scope("onvif://www.onvif.org/Profile")
        wsd.start()
        services = wsd.searchServices(scopes=[scope1])
        ipaddresses = []
        for service in services:
            ipaddress = re.search('(\d+|\.)+', str(service.getXAddrs()[0])).group(0)
            ipaddresses.append(ipaddress)

        wsd.stop()
        #  FIXME: Emulated connection
        server_ip = os.getenv("IP")
        self.lst.append(server_ip)

        return ipaddresses


finder = Finder()
