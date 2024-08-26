#  gw2pvo
This script pulls data directly from the GoodWe inverter and sends it directly to PVOutput **without** using the SEMS portal.

This version has been updated to work correctly in a Docker container and also comes with a Docker Compose reference. The container is available on Docker Hub as a multi-arch image under the name gw2pvo."

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
git clone https://github.com/madtempest/gw2pvo gw2pvo
cd gw2pvo/docker
docker build -t gw2pvo .
docker run --restart on-failure --name="gw2pvo" -e GW_IP_ADDRESS="10.10.100.253" -e GW_FAMILY="DT" -e GW_COMM_ADDR=0x7f -e PVO_SYSTEMID="12345" -e PVO_APIKEY="<insert string here>" -d gw2pvo 
```

## Todo
* Change the environment variables in Dockerfile to use a .env file instead
* The ability to swap between test and production mode containers where test is testing the connection to the inverter and production is uploading to PVOutput.org.
* Fix for the undefined variable: e_total_last.
* An SQLite database to support local data collection in case upload fails to allow later export and correct to PVOutpu.org.
* A "Powered by SunriseSunset.io," with lattitude and longitude based sunrise and sunset times to stop polling relentlessly overnight.
* Pull the latitude and longitude from pvoutput.org instead of them being environment variables.
* A "padding" variable to ensure that the script is running when first light arises (typical default is 30 mins either side of sunrise and set)
* Bash script for Crontab instead of Docker.
* A systemd unit to run this standalone rather than as Docker.
* Addition of Homebridge plugin using this code.



## Credits

https://github.com/lampra1/goodwe2pvoutput

https://github.com/Scampi-ml/goodwe2pvoutput

https://github.com/Janvier123/goodwe2pvoutput

https://github.com/windcrusader/gw2pvo
