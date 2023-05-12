#  goodwe2pvoutput
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



## Credits

https://github.com/Janvier123/goodwe2pvoutput
https://github.com/windcrusader/gw2pvo
