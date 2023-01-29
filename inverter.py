import asyncio
import goodwe
import logging
import sys
import socket
import time
import re
import pvo_api

# Set the level of logging
LOGLEVEL        = "INFO"                                        # Options: INFO,ERROR - Default: INFO

logging.basicConfig(
    format="%(asctime)-15s %(levelname)s: %(message)s",
    stream=sys.stderr,
    level=getattr(logging, LOGLEVEL, None),
)
logging.info("Starting the script")
logging.info("Start setting values")


# GoodWe Settings
GW_IP_ADDRESS   = "192.168.0.0"                                 # Example: 192.168.0.15
GW_FAMILY       = "DT"                                          # One of ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically
GW_COMM_ADDR    = None                                          # Usually 0xf7 for ET/EH or 0x7f for DT/D-NS/XS, or None for default value
GW_TIMEOUT      = 1                                             # time in seconds - default 1
GW_RETRIES      = 3                                             # times to retry - default 3
GW_INTERVAL     = 10                                            # Ready every # seconds, keep below 60

# PVoutput Settings
PVO_SYSTEMID    = "12345"                                       # The System ID from pvoutput.org
PVO_APIKEY      = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"   # The API key from pvoutput.org

# Settings some things - DO NOT EDIT
data            = []
e_day_last      = 0
tl              = time.localtime()
pvo             = pvo_api.PVOutputApi(PVO_SYSTEMID, PVO_APIKEY)


logging.info("End setting values")
logging.info("Start Main script")
logging.info("Start a connection to the inverter")
try:
    # fails when the inverter is offline at night
    inverter = asyncio.run(goodwe.connect(GW_IP_ADDRESS, GW_COMM_ADDR, GW_FAMILY, GW_TIMEOUT, GW_RETRIES))

except Exception as inst:
    # notify offline
    logging.error("Can't connect, asume offline :: %s", str(inst))
    sys.exit()

else:
    logging.info("Connected!")
    # inverter read succesfully
    logging.info("Model %s, Serial %s, Version %s", inverter.model_name, inverter.serial_number, inverter.software_version)
    response = asyncio.run(inverter.read_runtime_data())
    
    if (LOGLEVEL == "INFO"):
        logging.info("Start runtime_data")
        for sensor in inverter.sensors():
            if sensor.id_ in response:
                print(f"{sensor.id_}: \t\t {sensor.name} = {response[sensor.id_]} {sensor.unit}")
        logging.info("End runtime_data")

    
    # uncomment the lines below line if you want to pull inverter settings, this may not work on all models
    # See a raw example of what it can pull at: https://github.com/Janvier123/goodwe2pvoutput/tree/main/data_dump
    
    #response2 = asyncio.run(inverter.read_settings_data())
    #if (LOGLEVEL == "INFO"):
    #    logging.info("Start settings_data")
    #    for setting in inverter.settings():
    #        print(f"{setting.id_}: \t\t {setting.name} = {response2[setting.id_]} {setting.unit}")            
    #    logging.info("End settings_data")

    # reads -1 sometimes
    if (response['ppv'] >= 0 and response['e_day'] >= 0):
        e_day_last = response['e_day']
        logging.info("e_day_last: %s", e_day_last)

    # Goodwe is somewhat buggy, sometimes return 0 for total day energy. We don't want to see that in PVOutput
    if (response['e_day'] > 0):
        e_day = response['e_day']
    elif (e_day_last > 0):
        e_day = e_day_last
    else:
        e_day = 0
     
    logging.info("e_day: %s", e_day)
    
    
    # See https://pvoutput.org/help/api_specification.html#add-status-service
    # DO NOT SEND v5 unless it can get it from the outside, probably not. Please use the build in OpenWeatherMap from PVoutput.
    

    logging.info("Start PVoutput")
    logging.info("Adding the status")
    
    pvo.add_status(
        "{:04}{:02}{:02}".format(tl.tm_year, tl.tm_mon, tl.tm_mday),            # d - Output Date in YYYY:MM:DD
        "{:02}:{:02}".format(tl.tm_hour, tl.tm_min),                            # t - Time in HH:MM
        round(e_day * 1000),                                                    # v1 - Energy Generation
        response['e_total'],                                                    # v2 - Power Generation
        None,                                                                   # v3 - Energy Consumption
        None,                                                                   # v4 - Power Consumption
        None,                                                                   # v5 - Temperature
        response['vgrid'],                                                      # v6 - Voltage
        None,                                                                   # c1 - Cumulative Flag
        None,                                                                   # n - Net Flag
        None,                                                                   # v7 - Extended Value v7 (DONATION ONLY)
        None,                                                                   # v8 - Extended Value v8 (DONATION ONLY)
        None,                                                                   # v9 - Extended Value v9 (DONATION ONLY)
        None,                                                                   # v10 - Extended Value v10 (DONATION ONLY)
        None,                                                                   # v11 - Extended Value v11 (DONATION ONLY)
        None,                                                                   # v12 - Extended Value v12 (DONATION ONLY)
        None                                                                    # m1 - Text Message 1 (DONATION ONLY)
    )
    
    logging.info("Ending the status")
    
    logging.info("End PVoutput")
 
logging.info("End of script")