import threading
import time
from os import system
from subprocess import Popen
from time import sleep

import numpy as np

import Adafruit_DHT


class CommsManager:
    def __init__(self, phone_to, phone_from, twilio_key):
        # number format +90...
        # twilio key format ACe2fcd5d670cb1e60cc02fe712a20acbf:2f4bdd38d92a814247bcc42dce1c830e
        # TODO: change this
        self.phone_to = phone_to
        self.phone_from = phone_from
        self.twilio_key = twilio_key
        self.sound_cycle()

    def blink(self, dur, pin):
        """
        Led blinks for -dur- seconds
        5V comes from number -pin- from rpi
        """
        system("gpio -g mode " + str(pin) + " out")
        for i in range(dur):
            system("gpio -g write " + str(pin) + " 1")
            sleep(1)
            system("gpio -g write " + str(pin) + " 0")
            sleep(1)

    def buzzer(self, dur, pin):
        """
        Buzzer sings for -dur- seconds
        5V comes from number -pin- from rpi
        """
        system("gpio -g mode  " + str(pin) + " out")
        system("gpio -g write  " + str(pin) + " 1")
        sleep(dur)
        system("gpio -g write  " + str(pin) + " 0")

    def send_sms(self, message):
        if not self.phone_to:
            return
        sms_command = "curl -X POST 'https://api.twilio.com/2010-04-01/Accounts" \
                      "/ACe2fcd5d670cb1e60cc02fe712a20acbf/Messages.json'" + \
                      " --data-urlencode 'To=" + self.phone_to + "'" + \
                      " --data-urlencode 'From=" + self.phone_from + "'" + \
                      " --data-urlencode 'Body=" + message + "'" + \
                      " -u " + self.twilio_key
        p = Popen(sms_command, shell=True)
        p.communicate()

    def take_sample(self, dur, temp_file, hum_file):
        """
        Takes sample for -dur- seconds
        Saves samples to -temp_file- and -hum_file- as numpy array
        """
        temperature_arr = []
        humidity_arr = []

        for i in range(dur):
            try:
                humidity, temperature = Adafruit_DHT.read_retry(11, 4)
                temperature_arr.append(temperature)
                humidity_arr.append(humidity)
            except Exception as e:
                print e

        np.save(temp_file, np.array(temperature_arr))
        np.save(hum_file, np.array(humidity_arr))

    def take_single_sample(self):
        return Adafruit_DHT.read_retry(11, 4)

    def sound_cycle(self, host='proxima', ip='104.46.56.74', path='/home/proxima/'):
        system('python sound_recorder.py')
        send_command = 'rsync -avz -e ssh orig.wav ' + str(host) + '@' + str(ip) + ':' + str(path)
        threading.Timer(25, self.sound_cycle).start()
