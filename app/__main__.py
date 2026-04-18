from app.battery import get_power
from app.cpu import get_cpu_temps
from app.log import log_data
from datetime import datetime


def main():
    # temperature of cpu
    datas = get_cpu_temps()
    
    for data in datas:
        name, value = data
        
        logged_data = copy(data)
        logged_data["timestamp"] = datetime.now()

        log_data(data, "cpu_temperature")
    
if __name__ == "__main__":
    main()