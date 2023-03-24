import re
import os
import nmap3
from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from concurrent.futures import ThreadPoolExecutor
import netifaces


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
        self.lst = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.check_camera, ip)
                for ip in self.get_ips_from_urls(self.urls)
            ]
            for ip, result in zip(self.get_ips_from_urls(self.urls), futures):
                if result and ip not in self.lst:
                    self.lst.append(ip)
        em_ip_camera = os.getenv("IP")
        self.lst.append(em_ip_camera)
        return self.lst

    def check_camera(self, ip_address):
        nm = nmap.PortScanner()
        result = nm.scan(hosts=ip_address, arguments="-sn")
        if ip_address in result["scan"]:
            if result["scan"][ip_address]["status"]["state"] == "up":
                return True
        return False

    def get_ips_from_urls(self, urls):
        for url in urls:
            match = re.search(r"\d+\.\d+\.\d+\.\d+", url)
            if match:
                yield match.group(0)


finder = Finder()
