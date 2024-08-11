#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import goodwe
import logging
import sys
import socket
import time
import datetime
import re
import pvo_api
import os


# Set the level of logging
LOGLEVEL=os.environ['LOG_LEVEL']

logging.basicConfig(
    format="%(asctime)-15s %(levelname)s: %(message)s",
    stream=sys.stderr,
    level=getattr(logging, LOGLEVEL, None),
)

while True:
    if datetime.datetime.now().minute % 5 == 0:

        logging.info("Starting the script")
        logging.info("Start setting values")

        # GoodWe Settings
        GW_IP_ADDRESS=os.environ['GW_IP_ADDRESS']
        GW_PORT=os.environ['GW_PORT']
        GW_FAMILY=os.environ['GW_FAMILY']
        GW_COMM_ADDR=int(os.environ['GW_COMM_ADDR'], 16)
        GW_TIMEOUT=int(os.environ['GW_TIMEOUT'])
        GW_RETRIES=int(os.environ['GW_RETRIES'])
        GW_INTERVAL=int(os.environ['GW_INTERVAL'])

        # PVoutput Settings
        PVO_SYSTEMID=os.environ['PVO_SYSTEMID']
        PVO_APIKEY=os.environ['PVO_APIKEY']

        # Settings some things - DO NOT EDIT
        data=[]
        e_day_last=0
        tl=time.localtime()
        pvo=pvo_api.PVOutputApi(PVO_SYSTEMID, PVO_APIKEY)


        logging.info("End setting values")
        logging.info("Start Main script")
        logging.info("Start a connection to the inverter")

        try:
            # fails when the inverter is offline at night
            inverter=asyncio.run(goodwe.connect(GW_IP_ADDRESS, GW_PORT, GW_FAMILY, GW_COMM_ADDR, GW_TIMEOUT, GW_RETRIES))
        except Exception as inst:
            # notify offline
            logging.error("Can't connect, assume offline :: %s", str(inst))
            sys.exit()

        else:
            logging.info("Connected!")
            # inverter read succesfully
            logging.info("Model %s, Serial %s, Version %s", inverter.model_name, inverter.serial_number, inverter.firmware)
            response = asyncio.run(inverter.read_runtime_data())

            if (LOGLEVEL == "INFO"):
                logging.info("Start runtime_data")
                for sensor in inverter.sensors():
                    if sensor.id_ in response:
                        print(f"{sensor.id_}: \t\t {sensor.name} = {response[sensor.id_]} {sensor.unit}")
            logging.info("End runtime_data")

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

            today = "{:04}{:02}{:02}".format(tl.tm_year, tl.tm_mon, tl.tm_mday)
            now = "{:02}:{:02}".format(tl.tm_hour, tl.tm_min)

        # Try for c1=1
            if (response['e_total'] > 0):
                e_total = response['e_total']
            elif (e_total_last > 0):
                e_total = e_total_last
            else:
                e_total = 0

            logging.info("e_total: %s", e_total)


            if response.get('e_load_total') is not None:
                e_load_total = response['e_load_total']
                logging.info("e_load_total: %s", e_load_total)
                e_load_total = round(e_load_total * 1000)
            else:
                e_load_total = None

            if response.get('backup_ptotal') is not None:
                backup_ptotal = response['backup_ptotal']
            else:
                backup_ptotal = None

        # See https://pvoutput.org/help/api_specification.html#add-status-service
        # DO NOT SEND v5 unless it can get it from the outside, probably not. Please use the built-in OpenWeatherMap from PVoutput.

            logging.info("Start PVoutput")
            logging.info("Adding the status")

            pvo.add_status(
                today,            # d - Output Date in YYYY:MM:DD
                now,                            # t - Time in HH:MM
                round(e_total * 1000),                                                  # v1 - Energy Generation
                response['ppv'],                                                        # v2 - Power Generation
                e_load_total,                                             # v3 - Energy Consumption
                backup_ptotal,                                                          # v4 - Power Consumption
                None,                                                                   # v5 - Temperature
                response['vpv1'],                                                       # v6 - Voltage
                1,                                                                      # c1 - Cumulative Flag
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
            time.sleep(60)
