#!py -3.5

"""
MIT License

Copyright (c) 2016 William Tumeo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import argparse
import os.path
from maid import Maid, get_info
from maid import DataLoader, DataDownload
from yaml import load as yaml_load


# Add cli commands
parser = argparse.ArgumentParser(prog="Shiori", description="")
parser.add_argument("-r", "--remote", help="fetch remote data", action="store_true")
parser.add_argument("-p", "--path", metavar="data_path", help="path for data files")
parser.add_argument("-u", "--urlprefix", metavar="url", help="prefix domain for data")
parser.add_argument("-v", "--version", help="show version", action="store_true")
args = parser.parse_args()

DATA = args.path
CONF = None
CONF_F = 'configs.yml'
MODE = 'local'


def print_info():
    """Print version info and exit program."""
    print(get_info())
    sys.exit(0)


def set_remote():
    """Fetch and save config file from remote server."""
    global MODE
    global CONF_F

    MODE = 'remote'
    remote = DataDownload(DATA, args.urlprefix)
    CONF_F = remote.download(CONF_F)


def set_configs(remote=False):
    """Load local config file and save to global CONF."""
    global CONF

    with open(os.path.join(DATA, CONF_F), 'r') as cf:
        CONF = yaml_load(cf.read())
    del cf
    if remote:
        CONF['url-prefix'] = args.urlprefix


def shut_down(er):
    """Deprecated close method"""
    print("Estou morrendo :scream:")
    print("```shell\n{0}\n```".format(er))
    shiori.close()


def start_shiori():
    """Start Shiori bot"""
    shiori = Maid(CONF, DataLoader(CONF, MODE, DATA))
    shiori.create_tasks()
    shiori.run(CONF['discord']['token'])


if __name__ == '__main__':
    if args.version:
        print_info()
    if args.remote:
        set_remote()
        set_configs(True)
    else:
        set_configs()

    try:
        start_shiori()
    except Exception as er:
        shut_down(er)
