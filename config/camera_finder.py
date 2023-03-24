from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import Scope
import re


class Finder:
    def fetch_devices():
        wsd = WSDiscovery()
        scope1 = Scope("onvif://www.onvif.org/Profile")
        wsd.start()
        services = wsd.searchServices(scopes=[scope1])
        ipaddresses = []
        for service in services:
            ipaddress = re.search('(\d+|\.)+', str(service.getXAddrs()[0])).group(0)
            ipaddresses.append(ipaddress)

        wsd.stop()
        return ipaddresses

finder = Finder()
