import re
import os
import netifaces
from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery


class Finder:
    def __init__(self):
        self.started = False
        self.ips = []
        for iface in netifaces.interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(iface):
                self.ips.append(
                    netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["addr"]
                )
        self.scope = [".".join(ip.split(".")[:2]) for ip in self.ips]
        self.wsd = WSDiscovery()

    def start(self):
        self.wsd.start()
        self.ret = self.wsd.searchServices()
        self.onvif_services = [
            s for s in self.ret if str(s.getTypes()).find("onvif") >= 0
        ]
        self.urls = [ip for s in self.onvif_services for ip in s.getXAddrs()]
        self.ips = [
            ip for url in self.urls for ip in re.findall(r"\d+\.\d+\.\d+\.\d+", url)
        ]
        self.lst = [ip for ip in self.ips if ip.startswith("192.168.")]
        server_ip = os.getenv("IP")
        self.lst.append(server_ip)
        return self.lst


finder = Finder()
