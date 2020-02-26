# metrics.py
Scrypt for collecting metrics about some linux server.

## Usage
Extract file to directory where you will call it.
Change directory to where you unpacked file.
Make file executable with command:
```
> $ chmod +x metrics.py
```

Run the file with options:

* -c --cpu - for cpu usage info
* -s --sys - for system info
* -n --net - for network info
* -m --mem - for memoty usage info
* -d --disk - for disk usage info
* -h --help - for help

For example:
```
> $ ./metrics.py -c
```

Output:
```
> ========== CPU FREQUENCY ==========
> Physical cores: 1
>  Total cores: 2
>  Max Frequency: 0.00Mhz
>  Min Frequency: 0.00Mhz
>  Current Frequency: 3497.97Mhz
>  ========== CPU Usage Per Core: ==========
>  Core 0: 0.0%
>  Core 1: 100.0%
>  Total CPU Usage: 0.0%
> ========== CPU Metrics ==========
>  idle 182875.04
>  user 192.84
>  guest 0.0
>  iowait 122.76
>  stolen 0.0
>  system 203.33
```
