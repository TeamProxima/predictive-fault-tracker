#!/usr/bin/python

import argparse
import json
from wsgiref.simple_server import make_server

from constants import *
from db_manager import DBManager

args = None


def application(environ, start_response):
    path = environ['PATH_INFO'][1:]
    db_manager = DBManager(args.DBHOST, args.DBUSER, args.DBPASSWD, args.DBNAME)
    db_manager.db.commit()
    retval = json.dumps({'response': 'failed'})

    if path == 'sound.wav':
        start_response('200 OK', [('Content-type', 'application/audio')])
        fdesc = open(SYNCED_AUDIO_FILE_LOCATION, 'rb')
        block_size = 1024
        if 'wsgi.file_wrapper' in environ:
            t = environ['wsgi.file_wrapper'](fdesc, block_size)
        else:
            t = iter(lambda: fdesc.read(block_size), '')
        fdesc.close()
        return t
    else:
        start_response('200 OK', [('Content-type', 'application/json')])

    if path == 'train':
        fdesc = open(TRAIN_BUFFER_FILE, 'wb')
        fdesc.seek(0)
        fdesc.write("1")
        fdesc.close()
        retval = json.dumps({'train': 1})

    elif path == 'latest':
        retval = db_manager.latest()

    elif path == 'soundproblem':
        retval = db_manager.sound_alert()

    elif path == 'tempproblem':
        retval = db_manager.temp_alert()

    else:
        retval = db_manager.report(period=path)

    return retval


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mobile server settings')
    parser.add_argument('-sp', '--PORT', help='server port', type=int,
                        default=8080, required=False)
    parser.add_argument('-sip', '--IP', help='server ip', type=str,
                        default='', required=False)
    parser.add_argument('-dh', '--DBHOST', help='database host', type=str,
                        required=True)
    parser.add_argument('-du', '--DBUSER', help='database user', type=str,
                        required=True)
    parser.add_argument('-dp', '--DBPASSWD', help='database password', type=str,
                        required=True)
    parser.add_argument('-dn', '--DBNAME', help='database name', type=str,
                        required=True)
    args = parser.parse_args()
    make_server(args.IP, args.PORT, application).serve_forever()
