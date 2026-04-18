from datetime import datetime

from app.cpu import get_cpu_temps
from app.disk import get_all_disk_temps
from app.log import log_data
from app.sender import send_to_api
from config import HOSTIP, HOSTNAME


def run():
    datas = get_cpu_temps()
    
    send_datas = []
    
    for name, value in datas:
        logged_data = {
            "timestamp": datetime.now().isoformat(),
            "core": name,
            "temperature": value
        }

        log_data(logged_data, "cpu_temperature")
        
        send_data = {
            "type": "temperature",
            "source": "local",
            "host_name": HOSTNAME,
            "host_ip": HOSTIP,
            "device_type": "CPU",
            "name": name,
            "value": value
        }
        
        send_datas.append(send_data)
        
    datas = get_all_disk_temps()
    
    for name, value in datas.items():
        logged_data = {
            "timestamp": datetime.now().isoformat(),
            "core": name,
            "temperature": value
        }
        
        log_data(logged_data, "disk_temperature")

        real_name = name.strip("/").split("/")[1]

        if value is not None:
            send_data = {
                "type": "temperature",
                "source": "local",
                "host_name": HOSTNAME,
                "host_ip": HOSTIP,
                "device_type": "DISK",
                "name": real_name,
                "value": value,
                "meta": name
            }
            
            send_datas.append(send_data)
        
    if send_datas:    
        send_to_api(send_datas)
        
"""
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT NOT NULL,
            source TEXT NOT NULL,
            host_name TEXT NOT NULL,
            host_ip TEXT NOT NULL,
            target TEXT,
            device_type TEXT,
            name TEXT,
            value REAL,
            value_text TEXT,
            meta TEXT
"""
