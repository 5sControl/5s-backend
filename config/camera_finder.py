import re
import os
import subprocess
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
        self.lst = [
            ip
            for ip in self.ips
            if (ip.startswith("192.168."))
            and (ip is not None)
            and (self.check_camera(ip))
        ]
        server_ip = os.getenv("IP")
        self.lst.append(server_ip)
        return self.lst

    def check_camera(self, ip_address):
        result = subprocess.run(
            ["ping", "-c", "4", ip_address], capture_output=True, text=True
        )
        if (
            ("0% packet loss" in result.stdout)
            and ("100% pocket loss" not in result.stdout)
            and not (" 0 received" in result.stdout)
        ):
            return True
        else:
            return False


finder = Finder()
