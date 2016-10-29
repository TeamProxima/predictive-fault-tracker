#!/usr/bin/python

import argparse
from board_manager import BoardManager
from constants import *


def main():
    parser = argparse.ArgumentParser(description='Board client settings')
    parser.add_argument('-sp', '--PORT', help='server port', type=int,
                        default=80, required=False)
    parser.add_argument('-sip', '--IP', help='server ip', type=str,
                        default='', required=False)
    parser.add_argument('-pt', '--TO', help='phone to', type=str,
                        default='', required=False)
    parser.add_argument('-pf', '--FROM', help='phone from', type=str,
                        default='', required=False)
    parser.add_argument('-tk', '--TWKEY', help='twilio key', type=str,
                        default='', required=False)
    args = parser.parse_args()
    bm = BoardManager(args)
    bm.activate()


if __name__ == "__main__":
    main()
