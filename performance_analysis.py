from win32api import * 
import psutil, os
from tabulate import tabulate 
from time import sleep
import wmi

def main():
    # store all process for display
    all_processes = []
    
    # Constants
    headers = ["Username", "Cpu", "Memory", "Disk", "Network"]
    process_header =  ["process ID", "process Name"]
    
    MB = 1024 ** 2
    AVERAGE_BYTE_COUNT_TIME = 5

    # Method Calls from the win32api and psutils
    CPU = psutil.cpu_percent(2)
    AVAIL_MEM = psutil.virtual_memory().available / MB
    MEM = psutil.virtual_memory().total / MB
    MEM_USAGE = ((MEM - AVAIL_MEM) / MEM) * 100
    DISK_IO = psutil.disk_io_counters().count(AVERAGE_BYTE_COUNT_TIME)
    NAME = GetUserName()
    
    # String Creation
    MEMORY = f"{AVAIL_MEM:.2f}/{MEM:.2f} {MEM_USAGE:.0f}%"
    DISK_IO = f"{DISK_IO} R/W"
    if  not psutil.net_if_stats().get("Wi-Fi"):
        WIFISPEED = psutil.net_if_stats().get("Wi-Fi").speed
        WIFI = psutil.net_if_stats().get("Wi-Fi").count(AVERAGE_BYTE_COUNT_TIME)
        WIFI = f"{WIFI} R/W /{WIFISPEED}"
    else:
        WIFI = None
 
    # Initializing the wmi constructor
    f = wmi.WMI()
    
    # Iterating through all the running processes
    for process in f.Win32_Process():
        # Appending the P_ID and P_Name of the all_process list
        all_processes.append((f"{process.ProcessId:<10}", process.Name))

    # Table Creation
    column = [(NAME, CPU, MEMORY, DISK_IO, WIFI)]
    
    table = tabulate(column, headers=headers)
    process_table = tabulate(all_processes, headers=process_header) 
    
    # Table Display
    print(table) 
    print(process_table)

if __name__ == "__main__":
    main()