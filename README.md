#  goodwe2pvoutput
This script pulls data directly from the GoodWe inverter and sends it directly to PVOutput **without** using the Sems portal.
Please note that this script comes from a [fork](https://github.com/ASlatius/gw2mqtt-pvo), i only modified it and made a better guide based on [this](https://github.com/markruys/gw2pvo/) old script.


## Checking Requirements
- Check if **Python** is installed [More Info](https://www.scaler.com/topics/check-python-version/) 
- Check if **PIP** is installed [More Info](https://pip.pypa.io/en/stable/installation/) 
- Check if **Git** is installed [More Info](https://linuxize.com/post/how-to-install-git-on-raspberry-pi/)

You may run, just to be sure its all up-to-date:
```shell
sudo apt update && sudo apt full-upgrade -y && sudo apt autoremove -y && sudo apt-get autoclean -y
```
For this guide i will be using a **Raspberry Pi 3 Model B V1.2**. Others may work too.



## The OS
I will be using the **Raspberry Pi OS Lite (32-bit) without deskstop** using the **Raspberry Pi Imager**
[More info & how to](https://www.tomshardware.com/how-to/set-up-raspberry-pi)



## PVoutput.org
You will need a (free) account at [PVOutput](https://pvoutput.org). You will need a system to send the data to.
You can [create a system here](https://pvoutput.org/addsystem.jsp) or login to your account.
On your [account](https://pvoutput.org/account.jsp) **scroll down**, you will find the API section, set API Access to "**Enabled**".
**Note the API key** you will need it later.
**Scroll down**, you will see "**Registered Systems**", please note the "**System Id**" that you will be useing. Example: *53518*
Make sure the status is set to "**A**" *(Active)*.



## Installing 
Login to your Raspberry PI using Putty. I am using the default login for this example:
*Iam sure you will be able to google info about that topic.*

Make sure you are in your home directory, if not run this:
```shell
cd /home/pi
```

Clone the files:
```shell
git clone https://github.com/Janvier123/goodwe2pvoutput
```



## Editing the script
Go into the folder:
```shell
cd /home/pi/goodwe2pvoutput
```

Lets edit the file:
```shell
sudo nano inverter_read.py
```

Look for:
```ini
GW_IP_ADDRESS = "192.168.0.0"
```

Change to you own IP:

**NOTE:** *You can use [advanced ip scanner](https://www.advanced-ip-scanner.com/) to scan your network and pind the IP of your inverter.*
**NOTE:** *My inverter came with a website, so entering the ip gave me a website with some config data*


Look for:
```ini
GW_FAMILY = "DT"
```

**Options:**  *ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically*

On you inverter there should be a sticker, mine said: 
Model: **GW5048D-ES**.
Please note the **ES**, however in my SN there is also an "ES", so ive changed the GW_FAMILY to ES

Change to your whatever you may have.


Look for:
```ini
PVO_SYSTEMID    = "12345"
```
Change to your own **system ID** from PVOutput.

Look for:
```ini
PVO_APIKEY      = "21ef99aab2e79c7380aca48ae0aafe490cc1ff70c"
```
Change to your own API key from PVOutput, see above;
Press **CTRL + O**, press **ENTER**, **CTRL + X**


**OPTIONAL:**
You may want to tweak your script and send more data to PVOutput, for example if you are a donator on PVOutput.
You can send extended parameters: v7, v8, v9, v10, v11 and v12
For example, if you own a battery system you can send the batterly level, voltage, ... or whatever you want to keep record of.
[More info](https://pvoutput.org/help/donations.html#donations)



## Systemd service (Auto start)
So we want to run this as a service. As a bonus this will run if you unplug the power or restart the PI.

Open putty, login and type or copy the following:

```shell
sudo nano /etc/systemd/system/goodwe2pvoutput.service
```

Now copy the following:

```shell
[Unit]
Description=Read GoodWe inverter (UDP) and publish to PVOutput.org

[Service]
WorkingDirectory=/home/pi/goodwe2pvoutput
ExecStart=/usr/bin/python3 /home/pi/goodwe2pvoutput/inverter_read.py
Restart=always
RestartSec=300
User=goodwe2pvoutput

[Install]
WantedBy=multi-user.target
```

Please note the "**300**", this is the time *(in seconds)* before sending the next data. 
PVoutput [api](https://pvoutput.org/help/live_data.html#live-configuration-status-interval) has the following options:

>       5 minutes (Default) (or 300 sec)
>       10 minutes (or 600 sec)
>       15 minutes (or 900 sec)

I **highly** suggest leaving it at 300 for the best results.
Press **CTRL + O**, press **ENTER**, **CTRL + X**


Now run the following, line by line:
```shell
sudo useradd -m goodwe2pvoutput
sudo systemctl enable goodwe2pvoutput
sudo systemctl start goodwe2pvoutput
sudo systemctl status goodwe2pvoutput
sudo journalctl -u goodwe2pvoutput -f
```



## OpenWeatherMap
Create a account at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)
Go to **API Keys** and look for **Create key** enter a name, for example: **PVoutput**
A new key will be generated for you, **copy the API key**.



## Adding Temperature
The old [gw2pvo](https://github.com/markruys/gw2pvo/) script required that you uploaded the temperature based on your location, using **netatmo** or **Dark Sky**. 
For that we use the **Automatic Uploads** from PVOutput itself.

**NOTE:** *DO NOT upload the temperature from the inverter. This is the temperature from the inverter itself, but PVoutput expects outside temperature.*

Edit your system at the PVOutput Website, scroll down and look for **Automatic Uploads**
*You can find your systems at bottom or your [account](https://pvoutput.org/account.jsp).*

For this **example** i used the following values:

- **Primary Device**: Weather
- **Poll Interval**: 5 minutes
- **Shift Time**: None
- **Weather Device**: OpenWeatherMap
- **API Key**: < the key you copied >
- **Location** fill in your Latitude and longitude or press **Retrive**
- **Main Temperature**: Enabled

**Scroll down** and hit **Save**



## Final Notes
I am in **NO WAY** a Python programmer. However i do try my best to make things work, altho it may not be the best way to do it.
Feel free to open an ISSUE to give suggestions OR send me a pull request.
Forgive me for the bad english, Dutch is my main language ;)


## Credits
Original fork from:
https://github.com/ASlatius/gw2mqtt-pvo

Inspiration and guidance from:
PVoutput.org Community & API Help
https://github.com/marcelblijleven/goodwe
https://github.com/markruys/gw2pvo  
https://github.com/mletenay/home-assistant-goodwe-inverter  
