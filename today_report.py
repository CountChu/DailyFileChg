#
# FILENAME.
#       today_report.py - Today Report Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app saves a report from a given command in a file named 
#       with today's date, E.g., 2023-10-30.txt.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/4/22
#       Updated on 2023/10/30
#

import argparse
import subprocess
import datetime
import os
import sys

import pdb
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: Report the command "python file_chg.py -s" in a today's file of output directory.
        python today_report.py -cmd "python file_chg.py -s" -o output
'''
    parser = argparse.ArgumentParser(
                description=desc)

    parser.add_argument(
            '-o',
            dest='output',
            required=True,
            help='The output directory')       

    parser.add_argument(
            "--cmd",
            dest="command",
            required=True,
            help="Config file.")

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args

def run_it(cmd):
    print(cmd)

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(res.stdout.decode())
    
    if res.returncode != 0:
        print('Error! ----------------')
        print(res.stderr.decode())
        sys.exit(1)    

def main():

    #
    # Parse arguments
    #

    args = build_args()

    #
    # Check if the output directory exists.
    # If not, make it.
    #

    if not os.path.exists(args.output):
        print('The directory does not exist.')
        print('Making it.')
        print(args.output)
        os.mkdir(args.output)

    #
    # Build out_fn
    #

    out_fn = datetime.datetime.now().strftime('%Y-%m-%d')
    out_fn = '%s.txt' % out_fn 
    out_fn = os.path.join(args.output, out_fn)

    #
    # Run file_chg.py
    #

    cmd = args.command
    cmd = f'{cmd} > {out_fn}'

    run_it(cmd)

if __name__ == '__main__':
    main()
