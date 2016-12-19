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
import os
import argparse
from shiori import Maid, get_info
from shiori import DataLoader, DataDownload
from yaml import load as yaml_load
from yamldata import YamlData


ARGS = None
PATH = None
URL_PREFIX = None
SHIORI = None


class Shiori(object):
    """Main program class"""

    maid = None
    data_path = None
    configs = None
    config_file = None
    mode = None
    url_prefix = None


    def __init__(self, path, url_prefix=None):
        self.data_path = path
        self.config_file = 'configs.yml'
        self.mode = 'local'
        if url_prefix is not None:
            self.url_prefix = url_prefix


    def print_info(self):
        """Print version info and exit program."""
        print(get_info())
        sys.exit(0)


    def fetch_remote(self):
        """Fetch and save config file from remote server."""
        self.mode = 'remote'
        remote = DataDownload(self.data_path, self.url_prefix)
        self.config_file = remote.download(self.config_file)


    def set_configs(self):
        """Load local config file and save to global CONF."""
        with open(os.path.join(self.data_path, self.config_file), 'r') as cfg:
            self.configs = yaml_load(cfg.read())
        del cfg
        if self.url_prefix is not None:
            self.configs['url-prefix'] = self.url_prefix


    def shut_down(self, error):
        """Deprecated close method"""
        print("Estou morrendo :scream:")
        print("```shell\n{0}\n```".format(error))
        self.maid.close()


    def start(self):
        """Start Shiori bot"""
        loader = DataLoader(self.configs, self.mode, self.data_path)
        self.maid = Maid(self.configs, loader, YamlData(self.data_path))
        self.maid.create_tasks()
        self.maid.run(self.configs['discord']['token'])



def get_args():
    """Return CLI arguments"""
    parser = argparse.ArgumentParser(prog="Shiori", description="")
    parser.add_argument("-r", "--remote", help="fetch remote data", action="store_true")
    parser.add_argument("-p", "--path", metavar="data_path", help="path for data files")
    parser.add_argument("-u", "--url-prefix", metavar="url", help="prefix domain for data")
    parser.add_argument("-v", "--version", help="show version", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = get_args()
    PATH = os.getenv('SHIORI_PATH', ARGS.path)
    URL_PREFIX = os.getenv('SHIORI_URL_PREFIX', ARGS.url_prefix)
    SHIORI = Shiori(PATH, URL_PREFIX)

    if ARGS.version:
        SHIORI.print_info()
    if URL_PREFIX is not None:
        SHIORI.fetch_remote()
        
    SHIORI.set_configs()

    try:
        SHIORI.start()
    except KeyboardInterrupt as err:
        SHIORI.shut_down(err)
