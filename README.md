#  goodwe2pvoutput

## Introduction
This solution pulls data directly from the local GoodWe inverter and sends it directly to PVOutput **without** using the SEMS portal.

## Usage
You need an account at PVOutput.org.
You will need to populate the following variables.

### Location settings
* TZ = Your timezone in ISO8601 format. A list can be found here: 
* GW_LAT = Your latitude (You will need this for PVOutput as well)
* GW_LNG = Your longitude (You will need this for PVOutput as well)

### Inverter settings
* GW_IP_ADDRESS = This is set to the default address of 10.10.100.253. Set it to the IP address of your inverter.
* GW_PORT = This is set to the default port of 8899. Set it to the port of your inverter, likely still 8899.
* GW_FAMILY = One of ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically. You **must** set this for the script to function without errors.
* GW_COMM_ADDR = Usually 0xf7 for ET/EH or 0x7f for DT/D-NS/XS, or None for default value. You **must** set this for the script to function without errors.
* GW_TIMEOUT = time in seconds - default 1. Recommended is 5.
* GW_RETRIES = times to retry - default 3.
* GW_INTERVAL = Ready every number seconds, keep below 60.

### PVoutput settings
* PVO_SYSTEMID = Your System ID from pvoutput.org.
* PVO_APIKEY = Your API key from pvoutput.org.

### Logging settings
* LOG_LEVEL = The level of logging information as an option in Pythoin. Default is INFO.


## Features
* Collects data from the GoodWe inverter on the local network **without** needing to check the SEMS portal.
* "Powered by SunriseSunset.io," with lattitude and longitude based sunrise and sunset times to stop polling relentlessly overnight.
* Multi-Architecture Docker container (armhf, arm64, amd64).
* Docker Compose support.
* Bash script for Crontab instead of Docker.


## Future Enhancements
* The ability to swap between test and production modes
    where test is testing the connection and production is uploading to pvoutput.
* Fix for the undefined variable: e_total_last.
* Change to pull the latitude and longitude from pvoutput.org instead of them being environment variables.
* Addition of Homebridge plugin using this code.

## Background
I found a heap of undocumented components to this which made it more challenging to get working originally, and that kicked off an improvement program that has led to the current state. There was possibly also a change to the goodwe python library that was not accounted for in this implementation which probably contributed to that level of challenge and has been fixed in this implementation.

## Local Docker Build

```shell
docker build -t goodwe2pvoutput .
docker run --restart always --name="goodwe2pvoutput" -d goodwe2pvoutput
```

## Credits
https://github.com/lampra1/goodwe2pvoutput
https://github.com/Janvier123/goodwe2pvoutput
https://github.com/windcrusader/gw2pvo
