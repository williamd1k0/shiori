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
import maid
import yaml

parser = argparse.ArgumentParser(prog="Shiori", description="")
parser.add_argument("-r", "--remote", help="fetch remote data", action="store_true")
parser.add_argument("-p", "--path", metavar="data_path", help="path for data files")
parser.add_argument("-u", "--urlprefix", metavar="url", help="prefix domain for data")
parser.add_argument("-v", "--version", help="show version", action="store_true")
args = parser.parse_args()

DATA = args.path
CONF = None
REM = None
CONF_F = 'configs.yml'
MODE = 'local'

if args.version:
    print(maid.get_info())
    sys.exit(0)

if args.remote:
    MODE = 'remote'
    REM = maid.DataDownload(DATA, args.urlprefix)
    CONF_F = REM.download(CONF_F)

with open(os.path.join(DATA, CONF_F), 'r') as cf:
    CONF = yaml.load(cf.read())
del cf
CONF['url-prefix'] = args.urlprefix

shiori = maid.Maid(CONF, maid.DataLoader(CONF, MODE, DATA))


def shut_down(er):
    print("Estou morrendo :scream:")
    print("```shell\n{0}\n```".format(er))
    shiori.close()

try:
    shiori.create_tasks()
    shiori.run(CONF['discord']['token'])

except Exception as er:
    shut_down(er)
