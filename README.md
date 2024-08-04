#  goodwe2pvoutput

## Introduction


## Features
*Collects data from the GoodWe inverter on the local network **without** needing to check the SEMS portal.
*"Powered by SunriseSunset.io," with lattitude and longitude based sunrise and sunset times to stop polling relentlessly overnight.
*Multi-Architecture Docker container (armhf, arm64, amd64)
*Docker Compose support


## Future Enhancements
*The ability to swap between test and production modes
    where test is testing the connection and production is uploading to pvoutput
*Fix for the undefined variable e_total_last
*Change to pull the latitude and longitude from pvoutput.org instead of them being environment variables
*Addition of Homebridge plugin using this code

## Background
I found a heap of undocumented components to this which made it more challenging to get working originally, and that kicked off an improvement program that has led to the current state. There was possibly also a change to the goodwe python library that was not accounted for in this implementation which probably contributed to that level of challenge and has been fixed in this implementation.





This script pulls data directly from the GoodWe inverter and sends it directly to PVOutput **without** using the Sems portal.

Modified version from a [fork](https://github.com/Janvier123/goodwe2pvoutput) in order to work using Docker & send consumption data to pvo.


## Editing the script
Take a look at the [forked repo](https://github.com/Janvier123/goodwe2pvoutput)

## Docker x86-64
Runs every 5 minutes

```shell
docker build -t goodwe2pvoutput .
docker run --restart always --name="goodwe2pvoutput" -d goodwe2pvoutput
```

## More options 
Take a look at the [forked repo](https://github.com/Janvier123/goodwe2pvoutput)


“Powered by SunriseSunset.io“.

## Credits

https://github.com/Janvier123/goodwe2pvoutput

https://github.com/windcrusader/gw2pvo
