import json
import socket

from comms_manager import CommsManager
from constants import *


class BoardManager:
    def __init__(self, args):
        self.server_address = (args.IP, args.PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(15)
        self.sock.connect(self.server_address)
        self.cm = CommsManager(args.TO, args.FROM, args.TWKEY)

    def activate(self):
        """
        Continuously feeds server with sensor data and responds training requests
        """
        while True:
            try:
                humidity, temperature = self.cm.take_single_sample()
                packet = json.dumps({'scores': {'temperature': temperature,
                                                'humidity': humidity}})
                self.sock.send(packet)
                resp = self.sock.recv(1024)
                if resp:
                    resp = json.loads(resp)
                    if resp['response'] == -1:
                        self.cm.send_sms(
                            message='There is a temperature problem at station 2. For detailed'
                                    ' info siemenshackathon://scheme.net.siemenshackathon')
                        self.cm.blink(2, 17)
                    if resp['responsesound'] == -1:
                        self.cm.send_sms(
                            message='There might be a malfunction at station 2. For detailed '
                                    'info siemenshackathon://scheme.net.siemenshackathon')
                        self.cm.buzzer(2, 26)
                    if len([key for key, value in resp.iteritems() if key == 'train']):
                        # Train command makes a quick training through environment and sends
                        # results back
                        self.cm.take_sample(20, 'temperature', 'humidity')
                        # 'npy' field notify server for incoming training files
                        # Only temperature data used for ML
                        self.sock.send(json.dumps({'npy': 1, 'humid_file_name': HUMIDITY_DATA_FILE,
                                                   'temp_file_name': TEMPERATURE_DATA_FILE}))
                        fdesc = open(TEMPERATURE_DATA_FILE, 'rb')
                        data = fdesc.read(1024)
                        while data:
                            self.sock.send(data)
                            data = fdesc.read(1024)
                        fdesc.close()
            except Exception as e:
                print 'Error occurred during sending file: ', str(e)
                continue
