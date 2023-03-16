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
    try:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path))
    except:
        pass

    with open(path, 'wb') as f:
        f.write(data)

def append_file(path, data):
    with open(path, 'a') as f:
        msg = str(datetime.now()) +  ' [info] ' + data + '\n'
        f.write(msg)

def copy_file(source_file_path, destination_file_path):
    write_file(destination_file_path, read_file(source_file_path))


def update_record(file_dict: dict, path: str, create_folder = None):
    # for keep track of the files by storing the filename in file_dict
    for root, dirs , files in os.walk(path): 
        for dir in dirs:
            for file in os.listdir(os.path.join(path, dir)):
                    dir_file = os.path.join(dir, file)
                    file_source = os.path.join(path, dir_file)
                    print(dir)
                    if create_folder is not None:
                        print(os.path.join(create_folder, dir))
                        # if not os.path.exists(create_folder):
                        #     os.makedirs(os.path.join(create_folder, dir))

                    file_dict[os.path.join(dir, file)] = hashlib.md5(read_file(file_source)).hexdigest()



        # for dir in dirs:
        #     for file in os.listdir(os.path.join(path, dir)):
        #         if not file.endswith('.DS_Store'):
        #             file_source = os.path.join(path, os.path.join(dir, file))
        #             print(file_source)
        #             if file_source not in file_dict:
        #                 file_dict[os.path.join(dir, file)] = hashlib.md5(read_file(file_source)).hexdigest()


        # for file in files:
        #     if not file.endswith('.DS_Store'):
        #         file_source = os.path.join(root, file)
        #         if file_source not in file_dict:
        #             file_dict[file] = hashlib.md5(read_file(file_source)).hexdigest()
            

def synchronize(source_path: str, destination_path: str, log):
    # add key: filepath and value: hash to the SOURCE dict
    SOURCE = {}
    DESTINATION = {}
    update_record(SOURCE, source_path, create_folder=destination_path)
    # add key: filepath and value: hash to the DESTINATION dict
    update_record(DESTINATION, destination_path)
    print(SOURCE, DESTINATION)
    # synchronized 
    if SOURCE == DESTINATION:
        print("Synchronized")
    else:
        # synchronize
        print("Synchronizing")
        for key, val in SOURCE.items():
            if DESTINATION.get(key) is None or DESTINATION[key] != SOURCE[key]:
                cpy_msg = f"copying file {key} to {destination_path}" 
                if log:
                    append_file(log, cpy_msg)
                print(cpy_msg)
                copy_file(os.path.join(source_path, key), os.path.join(destination_path, key))
        
        for key in list(DESTINATION):
            if SOURCE.get(key) is None:
                DESTINATION.pop(key, None)
                rm_msg = f"removing file {key} from {destination_path}"
                if log:
                    append_file(log, rm_msg)
                print(rm_msg)
                rm_path = '/Users/anilcharles/Downloads/work/destination/hello/a.txt'
                os.remove(rm_path)
                os.rmdir(os.path.dirname(rm_path))


if __name__ == '__main__':
    main()