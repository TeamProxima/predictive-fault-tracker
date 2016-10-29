#!/usr/bin/python

import argparse

from board_server_manager import BoardServerManager


def main():
    parser = argparse.ArgumentParser(description='Board server settings')
    parser.add_argument('-sp', '--PORT', help='server port', type=int,
                        default=80, required=False)
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
    bsm = BoardServerManager(args)
    bsm.activate()


if __name__ == "__main__":
    main()
