import json
import socket
from subprocess import Popen

from analysis_manager import AnalysisManager
from constants import *
from db_manager import DBManager


class BoardServerManager:
    def __init__(self, args):
        self.args = args
        self.am = AnalysisManager()
        self.dm = DBManager(args.DBHOST, args.DBUSER, args.DBPASSWD, args.DBNAME)
        self.ip = args.IP
        self.port = args.PORT
        self.address = (self.ip, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.flag = 0

    def activate(self):
        try:
            self.sock.bind(self.address)
            self.sock.settimeout(3)
            self.sock.listen(1)
            while True:
                try:
                    conn, addr = self.sock.accept()
                    print 'Connected to: ' + str(addr)
                    data = conn.recv(1024)
                    while data:
                        fdesc = open(TRAIN_BUFFER_FILE, 'rb')
                        fdesc.seek(0)
                        self.flag = fdesc.read(1)
                        fdesc.close()
                        sensor_info = json.loads(data)
                        if 'npy' in sensor_info:
                            npy_data = conn.recv(1024)
                            conn.settimeout(4)
                            fdesc = open(sensor_info['temp_file_name'], 'wb')
                            while npy_data:
                                try:
                                    fdesc.write(npy_data)
                                    npy_data = conn.recv(1024)
                                except:
                                    break
                            fdesc.close()
                            self.train_models()
                            conn.settimeout(None)
                        if 'scores' in sensor_info:
                            resp_temp, resp_sound = self.get_test_results(sensor_info)
                            if self.flag == '1':
                                resp_json = json.dumps(
                                    {'response': resp_temp, 'responsesound': resp_sound,
                                     'train': 1})
                                fdesc = open(TRAIN_BUFFER_FILE, 'wb')
                                fdesc.seek(0)
                                fdesc.write('0')
                                fdesc.close()
                                self.flag = 0
                            else:
                                resp_json = json.dumps(
                                    {'response': resp_temp, 'responsesound': resp_sound})
                            conn.send(resp_json)
                            self.dm.cursor.execute(
                                self.dm.get_insert_query('user_history', sensor_info['scores']))
                            self.dm.db.commit()
                        data = conn.recv(1024)

                except Exception as e:
                    print e
                    continue

        except Exception as e:
            print e

    def train_models(self):
        print('Train started')
        model = self.am.get_trained_model_from_file(
            TEMPERATURE_NPY_FILE_LOCATION, TYPE_TEMP)
        self.am.save_model(model, TEMPERATURE_MODEL_FILE_LOCATION)
        p = Popen('aubiomfcc {} > {}'.format(SYNCED_AUDIO_FILE_LOCATION,
                                             MFCC_FEATURE_FILE_LOCATION),
                  shell=True)
        p.communicate()
        p = Popen('python mfcc_parser.py {}'.format(MFCC_FEATURE_FILE_LOCATION),
                  shell=True)
        p.communicate()
        model = self.am.get_trained_model_from_file(FEATURE_NPY_FILE_LOCATION,
                                                    TYPE_SOUND)
        self.am.save_model(model, SOUND_MODEL_FILE_LOCATION)
        print('Train finished')

    def get_test_results(self, sensor_info):
        print('Test started')
        model = self.am.load_model(TEMPERATURE_MODEL_FILE_LOCATION)
        resp_temp = self.am.predict(model, sensor_info['scores']['temperature'])[0]
        if resp_temp == 1:
            self.dm.cursor.execute(
                self.dm.get_insert_query('temp_history', {'problem': 0}))
        else:
            self.dm.cursor.execute(
                self.dm.get_insert_query('temp_history', {'problem': 1}))
        p = Popen('sudo aubiomfcc {} > {}'.format(SYNCED_AUDIO_FILE_LOCATION,
                                                  MFCC_FEATURE_FILE_LOCATION),
                  shell=True)
        p.communicate()
        p = Popen('python mfcc_parser.py {}'.format(MFCC_FEATURE_FILE_LOCATION),
                  shell=True)
        p.communicate()
        is_problem = self.am.check_for_problem_from_file(FEATURE_NPY_FILE_LOCATION)
        if is_problem:
            resp_sound = -1
            self.dm.cursor.execute(
                self.dm.get_insert_query('sound_history', {'problem': 1}))
        else:
            self.dm.cursor.execute(
                self.dm.get_insert_query('sound_history', {'problem': 0}))
            resp_sound = 1
        print('Test finished')
        return resp_temp, resp_sound
