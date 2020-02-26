#!/usr/bin/python3

import psutil, platform, sys, argparse, socket
from datetime import datetime

def get_size(bytes):
    """
    Scale bytes to ist proper format

    eg:
    4567890 => '4,6MB'
    """
    divider = 1024
    for data in ["", "K", "M", "G", "T", "P"]:
        if bytes < divider:
            return f"{bytes:.2f}{data}B"
        bytes /= divider

parser = argparse.ArgumentParser(
        description = 'Shows system metrics and info.')
parser.add_argument('-c', '--cpu', action='store_true', 
        help='Shows cpu usage info')
parser.add_argument('-s', '--sys', action='store_true',
        help='Shows system info')
parser.add_argument('-m', '--mem', action='store_true',
        help='Shows memory usage info')
parser.add_argument('-d', '--disk', action='store_true',
        help='Shows disk usage info')
parser.add_argument('-n', '--net', action='store_true',
        help='Shows network info')

args = parser.parse_args()
if args.cpu:
    cpufreq = psutil.cpu_freq()
    print('='*10, 'CPU FREQUENCY', '='*10)
    print('Physical cores:', psutil.cpu_count(logical=False),'\n',
          'Total cores:', psutil.cpu_count(logical=True),'\n',
          f'Max Frequency: {cpufreq.max:.2f}Mhz\n',
          f'Min Frequency: {cpufreq.min:.2f}Mhz\n',
          f'Current Frequency: {cpufreq.current:.2f}Mhz\n',
           '='*10,'CPU Usage Per Core:', '='*10)
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f' Core {i}: {percentage}%')
    print(f' Total CPU Usage: {psutil.cpu_percent()}%') 
    cputimes = psutil.cpu_times()
    print('='*10, 'CPU Metrics', '='*10)
    print(f' idle {cputimes.idle}\n',
          f'user {cputimes.user}\n',
          f'guest {cputimes.guest}\n',
          f'iowait {cputimes.iowait}\n',
          f'stolen {cputimes.steal}\n',
          f'system {cputimes.system}\n')

if args.sys:
    pname = platform.uname()
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print('='*10, 'SYSTEM INFORMATION', '='*10)
    print(f' System: {pname.system}\n',
          f'Node Name: {pname.node}\n',
          f'Release: {pname.release}\n',
          f'Version: {pname.version}\n',
          f'Machine: {pname.machine}\n',
          f'Processor: {pname.processor}\n',
          f'Boot Time: {bt.year}/{bt.month}/{bt.day}', 
          f'{bt.hour}:{bt.minute}:{bt.second}')

if args.mem:
    svmem = psutil.virtual_memory()
    print('='*10, 'MEMORY', '='*10)
    print(f"Total: {get_size(svmem.total)}\n",
          f'Available: {get_size(svmem.available)}\n',
          f'Used: {get_size(svmem.used)}\n',
          f'Percentage: {svmem.percent}%\n')
    print('='*10, 'SWAP', '='*10)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}\n",
          f"Free: {get_size(swap.free)}\n",
          f"Used: {get_size(swap.used)}\n",
          f"Percentage: {swap.percent}%\n")  

if args.disk:
    pdisk = psutil.disk_partitions()
    udisk = psutil.disk_usage('/')
    iocount = psutil.disk_io_counters()
    for partition in pdisk:
        print(f'  Device:          {partition.device}\n',
              f' Mountpoint:       {partition.mountpoint}\n',
              f' File system type: {partition.fstype}\n')
        try:
            part_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f'   Total Size: {get_size(part_usage.total)}\n',
              f'  Used:       {get_size(part_usage.used)}\n',
              f'  Free:       {get_size(part_usage.free)}\n',
              f'  Percentage: {part_usage.percent}%\n')

    print(f' Total disk usage:\n',
          f'Total size: {get_size(udisk.total)}\n',
          f'Used:       {get_size(udisk.used)}\n',
          f'Free:       {get_size(udisk.free)}\n',
          f'Percentage: {udisk.percent}%\n',
          f'Read count: {iocount.read_count}\n',
          f'Write count:{iocount.write_count}\n',
          f'Read bytes: {get_size(iocount.read_bytes)}\n',
          f'Write bytes:{get_size(iocount.write_bytes)}\n')


if args.net:
    int_map = {
            socket.AF_INET: 'IPv4',
            socket.AF_INET6: 'IPv6',
            psutil.AF_LINK: 'MAC'}

    netio = psutil.net_io_counters(pernic=True)
    netstat = psutil.net_if_stats()
    netaddr = psutil.net_if_addrs()
    for nic, addr in netaddr.items():
        print(f'{nic}:\n')
        if nic in netstat:
            st = netstat[nic]
            print('Stats:')
            print(f'Speed={get_size(st.speed)}MB, duplex={st.duplex}, mtu={st.mtu}, up={"YES" if st.isup else "NO"}')
        if nic in netio:
            io = netio[nic]
            print('Incoming:')
            print(f'Bytes: {get_size(io.bytes_recv)}, pkts: {io.packets_recv},')
            print(f'errs: {io.errin}, drops: {io.dropin}')
            print('Outgoing:')
            print(f'Bytes: {get_size(io.bytes_sent)}, pkts: {io.packets_sent},')
            print(f'errs: {io.errout}, drops: {io.dropout}')
        for ad in addr:
            print(f'{int_map.get(ad.family,ad.family)}:  ')
            print(f'Address:    {ad.address}\n',
                  f'Broadcast:  {ad.broadcast}\n',
                  f'Netmask:    {ad.netmask}\n')

