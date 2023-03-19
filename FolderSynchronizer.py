#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 18:50:20 2023

@author: anilcharles
"""


import argparse
import sys
import os 
import time
import hashlib
from datetime import datetime 

SOURCE = {}
DESTINATION = {}

def main():

    parser = argparse.ArgumentParser(
                        prog='Folder Synchronizer (source and replica)',
                        description='Synchronizes contents between source and destination folder',)

    parser.add_argument('-s', '--source', help='provide the source folder directory')
    parser.add_argument('-d', '--destination', help='provide the destination folder directory')
    parser.add_argument('-i', '--interval', help='provide the synchronization interval in seconds')
    parser.add_argument('-l', '--log', help='add logs to file specified')



    args = parser.parse_args()
    args, unknown = parser.parse_known_args()
    if unknown:
        print('\nunknown argument please try the following arguments\n\n')
        parser.print_help()
    if len(sys.argv[1:])==0:
        parser.print_help()

    process(args)

   

def process(args):
    if args.source and args.destination:
        print(args.source, args.destination)
        try:
            while True:
                synchronize(args.source, args.destination, args.log)
                time.sleep(int(args.interval))
        except KeyboardInterrupt:
            pass
    else:
        raise Exception('requires source, destination and sync interval')

def read_file(path):
    with open(path, 'rb') as f:
        return f.read()

def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def append_file(path, data):
    with open(path, 'a') as f:
        msg = str(datetime.now()) +  ' [info] ' + data + '\n'
        f.write(msg)

def copy_file(source_file_path, destination_file_path):
    write_file(destination_file_path, read_file(source_file_path))

def update_record(source, destination):
    global SOURCE
    global DESTINATION
    SOURCE = {}
    DESTINATION = {}
    for root, _, files in os.walk(source):
        directory = root.split(source)[1][1:]
        if len(directory) > 1:
            SOURCE[directory] = hashlib.md5(directory.encode()).hexdigest()
            
        for file in files:
            SOURCE[os.path.join(directory, file)] = hashlib.md5(read_file(os.path.join(root, file))).hexdigest()

    for root, _, files in os.walk(destination):
        directory = root.split(destination)[1][1:]
        if len(directory) > 1:
            DESTINATION[directory] = hashlib.md5(directory.encode()).hexdigest()
            
        for file in files:
            DESTINATION[os.path.join(directory, file)] = hashlib.md5(read_file(os.path.join(root, file))).hexdigest()


def synchronize(source: str, destination: str, log):
    update_record(source, destination)
    if SOURCE == DESTINATION:
        print("synchronized")
    else:
        for key, val in SOURCE.items():
            s = os.path.join(source, key)
            d = os.path.join(destination, key)     
            # check key is present in destination
            if DESTINATION.get(key) is None or DESTINATION[key] != SOURCE[key]:
                # if it's a directory, create the folder in destination.
                if os.path.isdir(s):
                    if not os.path.exists(d):
                        md_msg = f"creating folder {key} in {d}"
                        os.makedirs(d)
                        if log:
                            append_file(log, md_msg) 
                        print(md_msg)
                else:
                    cpy_msg = f"copying file {key} to {d}"
                    copy_file(s,d)
                    if log:
                        append_file(log, cpy_msg) 
                    print(cpy_msg)
                    
            DESTINATION[key] = val
            
        # folder/files in destination folder not present in source must be removed
        for key in list(sorted(DESTINATION, reverse=True)):
            s = os.path.join(source, key)
            d = os.path.join(destination, key)   
            if SOURCE.get(key) is None:
                if os.path.isdir(d):
                    rm_msg = f"removing folder {key} from {d}"
                    os.rmdir(d)
                    if log:
                        append_file(log, rm_msg)
                    print(rm_msg)
                if os.path.isfile(d):
                    rm_file = f"removing file {key} from {d}"
                    os.remove(d)
                    if log:
                        append_file(log, rm_file)
                    print(rm_file)
                DESTINATION.pop(key, None)


if __name__ == '__main__':
    main()