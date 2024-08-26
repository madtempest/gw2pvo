#  goodwe2pvoutput
This script pulls data directly from the GoodWe inverter and sends it directly to PVOutput **without** using the SEMS portal.

This version has been updated to work correctly in a Docker container and also comes with a Docker Compose reference.

To support the Docker Compose reference, this script now uses environment variables.

Sensible defaults for variables are pre-built into the container and are noted below in the required variables:

* GW_IP_ADDRESS="10.10.100.253" (Default)
* GW_PORT="8899" (Default)
* GW_FAMILY=None (Default) One of ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically.
* GW_COMM_ADDR=None (Default) Usually 0xf7 for ET/EH or 0x7f for DT/D-NS/XS, or None for default value
* GW_TIMEOUT="1" (Default) tTme in seconds
* GW_RETRIES="3" (Default) Timmes to retry
* GW_INTERVAL="10" (Default) Ready every # seconds, keep below 60
* PVO_SYSTEMID="" See PVOutput.org for how to get this
* PVO_APIKEY="" See PVOutput.org for how to get this
* LOG_LEVEL="INFO" (Default)

## PVoutput.org
You will need a (free) account at PVOutput. You will need a system to send the data to. You can create a system here or login to your account. On your account scroll down, you will find the API section, set API Access to "Enabled". Note the API key you will need it later.

Scroll down, you will see "Registered Systems", please note the "System Id" that you will be useing. Example: 53518 Make sure the status is set to "A" (Active).

## OpenWeatherMap
Create a account at OpenWeatherMap Go to API Keys and look for Create key enter a name, for example: PVoutput A new key will be generated for you, copy the API key.

## Adding Temperature
The old gw2pvo script required that you uploaded the temperature based on your location, using netatmo or Dark Sky. For that we use the Automatic Uploads from PVOutput itself.

NOTE: DO NOT upload the temperature from the inverter. This is the temperature from the inverter itself, but PVoutput expects outside temperature.

Edit your system at the PVOutput Website, scroll down and look for Automatic Uploads You can find your systems at bottom or your account.

For this example I used the following values:

* Primary Device: Weather
* Poll Interval: 5 minutes
* Shift Time: None
* Weather Device: OpenWeatherMap
* API Key: < the key you copied >
* Location fill in your Latitude and longitude or press Retrive
* Main Temperature: Enabled
* Scroll down and hit Save


## Docker
Runs every 5 minutes

```shell
docker build -t goodwe2pvoutput .
docker run --restart on-failure --name="goodwe2pvoutput" -d goodwe2pvoutput -e -e -e -e -e -e -e -e -e 
```

## More options 
Take a look at the [forked repo](https://github.com/Janvier123/goodwe2pvoutput)



## Credits

https://github.com/lampra1/goodwe2pvoutput

https://github.com/Scampi-ml/goodwe2pvoutput

https://github.com/Janvier123/goodwe2pvoutput

https://github.com/windcrusader/gw2pvo
