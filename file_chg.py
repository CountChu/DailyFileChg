#
# FILENAME.
#       file_chg.py - File Change Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app lists files that were updated or created on a certain day.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2022/4/10
#       Updated on 2023/10/30
#

import argparse
import glob, os
from datetime import datetime
import yaml
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
import pdb

br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: Display file changes today.
        python file_chg.py
        
    Usage 2: Display file changes on 2022/2/21
        python file_chg.py --ymd 20220221
    
    Usage 3: Display file changes today in silience mode.
        python file_chg.py -s
    
    Usage 4: Display file changes today by a given YAML config.
        python file_chg.py -c config-YOUR-NAME.yaml
'''

    parser = argparse.ArgumentParser(
                description='desc')

    parser.add_argument(
            "-c",
            dest="config",
            default="config.yaml",
            help="Config file.")

    parser.add_argument(
            "--ymd",
            dest="yyyymmdd",
            required=False,
            help="E.g., 20220221")    

    parser.add_argument(
            '--test',
            dest='test',
            action='store_true',
            help='Test it.')

    parser.add_argument(
            '-s',
            dest='silence',
            action='store_true',
            help='Silience mode. Do not display much messages')       

    #
    # Check arguments and return.
    #

    args = parser.parse_args()

    return args

def filter_files(fn_ls, rules):
    spec = PathSpec.from_lines(GitWildMatchPattern, rules)
    out = []
    for fn in fn_ls:
        if not spec.match_file(fn):
            out.append(fn)

    return out

def shorten_path(dn, shortPaths):
    for shortPath in shortPaths:
        if dn.find(shortPath['path']) == 0:
            dn = dn.replace(shortPath['path'], shortPath['short'])
            break
    return dn


def collect_today_files(args, cfg, home, home2, today_yyyymmdd):

    #
    # Collect all files.
    #

    dn = os.path.join(home, home2)
    print('='*80)
    print('Collecting all files under:')
    print(dn)
    fn_ls = glob.glob(dn+'/**/*', recursive=True)
    print('')
    if not args.silence:
        print('There are %d files' % len(fn_ls))

    #
    # Filter ignore list.
    #

    if not args.silence:
        print('Filter ignored files...')
    fn_ls = filter_files(fn_ls, cfg['ignores'])
    if not args.silence:
        print('There are %d files after filtering' % len(fn_ls))
    #
    # Sort files by modified time.
    #

    if not args.silence:
        print('Sorting files by modified time...')
    fn_ls.sort(key=os.path.getmtime, reverse=True)

    #
    # Get today changed files.
    #

    today_fn_ls = []
    for fn in fn_ls:
        t = os.path.getmtime(fn)
        dt = datetime.fromtimestamp(t)
        yyyymmdd = dt.strftime('%Y%m%d')
        if yyyymmdd == today_yyyymmdd:
            today_fn_ls.append(fn)
        else:
            break

    #today_fn_ls = fn_ls         # for testing

    #
    # fileStateList = [fileState]
    # fileState = {'path', 'date', 'time', 'shortPath'}
    #        

    fileStateList = [] 
    for fn in today_fn_ls:
        fileState = {}
        t = os.path.getmtime(fn)
        dt = datetime.fromtimestamp(t)
        fileState['path'] = fn 
        fileState['date'] = dt.strftime('%Y%m%d')
        fileState['time'] = dt.strftime('%H:%M')
        fileState['shortPath'] = fn[len(home)+1:]
        fileStateList.append(fileState)

    if not args.silence:
        print('I updated %d files in %s today' % (len(fileStateList), home2))
    '''
    for fileState in reversed(fileStateList):
        print('%s %s' % (fileState['time'], fileState['shortPath']))
    print('')
    '''

    if not args.silence:
        print('Decorating files...')
    last_dn = ''
    for fileState in reversed(fileStateList):
        dn = os.path.dirname(fileState['shortPath'])
        bn = os.path.basename(fileState['shortPath'])

        short_dn = shorten_path(dn, cfg['shortPaths'])

        if last_dn != short_dn:
            print('')
            print(short_dn)
        last_dn = short_dn 
        print('%s | %s' % (fileState['time'], bn))
    print('')

def main():

    #
    # Parse arguments
    #

    args = build_args()

    #
    # Load config.yaml
    #

    f = open(args.config, 'r')
    cfg = yaml.load(f, Loader=yaml.CLoader)
    f.close()

    #
    # Get today_yyyymmdd
    # 

    today_yyyymmdd = datetime.now().strftime('%Y%m%d')
    if args.yyyymmdd != None:
        today_yyyymmdd = args.yyyymmdd
    print('today_yyyymmdd = %s' % today_yyyymmdd)
    print('')

    if args.test:
        home = {
            'base': '/Users/visualge/Dropbox/CodeLearn/2023/2303-OP-TEE',
            'dir': 'images',
            }
        collect_today_files(args, cfg, home['base'], home['dir'], today_yyyymmdd)
        print('')

    else:
        for home in cfg['homes']:
            collect_today_files(args, cfg, home['base'], home['dir'], today_yyyymmdd)
            print('')

if __name__ == '__main__':
    main()  
