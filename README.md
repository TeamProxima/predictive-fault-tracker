# Predictive Fault Tracker

### :trophy: 1st place at Siemens Hackathon :trophy:

Predictive fault detection system that adapts to the environment and tracks for anomalies in the sound and temperature

This application was originally made for a hackathon held by Siemens in 2016 and got the grand prize.


## How does it work?
The system listens for environment sound, temperature and humidity. It trains an outlier detection model with raw temperature, humidity, and also with sound features that are extracted by MFCC method. When it detects an anomaly in any of the input data, it notifies the user from mobile application.

## Team
 - Baris Ozkuslar - [@Epokhe](https://github.com/Epokhe)
 - Doganalp Ergenc - [@d0d0d0](https://github.com/d0d0d0)
 - Emre Yigit Alparslan - [@EmreYigitAlparslan](https://github.com/EmreYigitAlparslan)
 - Oguzhan Unlu - [@oguzhanunlu](https://github.com/oguzhanunlu)


## Tools and Technologies
 - Raspberry Pi
 - USB Microphone
 - Temperature/Humidity sensor kit
 - Adafruit DHT library for sensor communication
 - Aubiomfcc for MFCC sound feature extraction
 - Sklearn for machine learning
 - Swift and charts library for iOS app
 - uWSGI & MySQL for web backend


