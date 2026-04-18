from datetime import datetime
from app.battery import get_power
from app.cpu import get_cpu_temps
from app.log import log_data
from app.sender import send_to_api
from config import HOSTIP, HOSTNAME
import os

os.umask(0o022)

def main():
    datas = get_cpu_temps()
    
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
        
        send_to_api(send_data)
        
    
if __name__ == "__main__":
    main()

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
