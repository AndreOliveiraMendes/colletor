import xml.etree.ElementTree as ET

import requests

from config import ROUTER_PASS, ROUTER_URL, ROUTER_USER


class RouterClient:
    def __init__(self):
        self.base = ROUTER_URL
        self.user = ROUTER_USER
        self.password = ROUTER_PASS
        self.session = requests.Session()

    def login(self):
        self.session.post(f"{self.base}/login", data={
            "username": self.user,
            "password": self.password
        })

    def get_devices(self):
        res = self.session.get(
            f"{self.base}/?_type=menuData&_tag=dhcp4s_dhcphostinfo_m.lua"
        )

        root = ET.fromstring(res.text)

        devices = []

        for inst in root.findall(".//Instance"):
            data = {}
            names = inst.findall("ParaName")
            values = inst.findall("ParaValue")

            for n, v in zip(names, values):
                if not n.text:
                    continue
                key = n.text.split('.')[-1]
                data[key] = v.text

            devices.append(data)

        return devices