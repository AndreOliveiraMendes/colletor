from app.battery import get_power
from app.cpu import get_cpu_temps
from app.log import log_data


def main():
    # temperature
    data = get_cpu_temps()
    
    print(data)
    
if __name__ == "__main__":
    main()