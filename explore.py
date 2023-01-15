#! /usr/bin/python3

import csv
import fnmatch
import getpass
import optparse
import os
import pprint
import re
import string
import subprocess
import sys
import time

from collections import defaultdict
from collections import Counter

file_request_counts = defaultdict(int)
file_request_sizes = defaultdict(float)
ip_address_sizes = defaultdict(float)

#-----------------------------------------------------------------------

def process_one_file(filename):
    print("")
    print("Processing " + filename)
    with open(filename, 'r') as f:
        # Use counter to short-circuit log file reading during development
        counter = 0
        for row in csv.reader(f, delimiter='|'):
            ip_address = row[4]
            file_requested = row[5]
            file_size_in_mb = float(row[6]) / 1024.0 / 1024.0
            file_request_counts[file_requested] += 1
            file_request_sizes[file_requested] += file_size_in_mb
            ip_address_sizes[ip_address] += file_size_in_mb
            # Use counter to short-circuit log file reading during development
            counter = counter + 1
            # if (counter > 5250):
            #     break
    print("Requested " + str(len(file_request_counts)) + " distinct files")
    print("Requests from " + str(len(ip_address_sizes)) + " distinct IP addresses")

#-----------------------------------------------------------------------

def print_summary():
    print("")
    print("ip_address_sizes (in MB) is")
    sorted_ip_address_sizes = sorted(ip_address_sizes.items(), key = lambda kv: kv[1], reverse=True)
    pprint.pprint(sorted_ip_address_sizes[:15])
    print("")
    print("file_request_sizes (in MB) is")
    sorted_file_request_sizes = sorted(file_request_sizes.items(), key = lambda kv: kv[1], reverse=True)
    pprint.pprint(sorted_file_request_sizes[:15])
    print("")
    print("file_request_counts is")
    sorted_file_request_counts = sorted(file_request_counts.items(), key = lambda kv: kv[1], reverse=True)
    pprint.pprint(sorted_file_request_counts[:15])

#-----------------------------------------------------------------------

def explore(args = []):
    help_text = """%prog [options] [file(s)]
Explore data in JFrog artifactory access logs.   Use -h for help."""
    parser = optparse.OptionParser(usage=help_text)
    # parser.add_option("-a", "--all", action="store_true", default=False, help="process all files")
    options, files = parser.parse_args()
    # print("Options are " + str(options))
    # print("Files are " + str(files))
    start_time = time.time()
    for file in files:
        process_one_file(file)
        current_time = time.time()
        elapsed_time = current_time - start_time
        if (elapsed_time > 90):
            start_time = current_time
            elapsed_time = 0
            print_summary()
        else:
            print("Elapsed time is " + str(elapsed_time))
    print_summary()

#-----------------------------------------------------------------------

if __name__ == "__main__": explore(sys.argv[1:])
