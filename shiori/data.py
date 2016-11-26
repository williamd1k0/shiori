
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

import os
from urllib import request, parse
import yaml


class DataDownload(object):
    """Class to download remote data."""

    def __init__(self, path, url_prefix=''):
        if not os.path.isdir(path):
            os.makedirs(path)
        self.data_path = path
        self.prefix = url_prefix
        self.last = None


    def download(self, url, desc=None, progress=True):
        """Download and save data."""
        try:
            full_url = self.prefix+'/'+url
            u = request.urlopen(full_url)

            scheme, netloc, path, query, fragment = parse.urlsplit(full_url)
            filename = os.path.basename(path)
            if not filename:
                filename = full_url.split('/')[-1]
            if desc:
                filename = desc

            with open(os.path.join(self.data_path, filename), 'wb') as f:
                meta = u.info()
                meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
                meta_length = meta_func("Content-Length")
                file_size = None
                if meta_length:
                    file_size = int(meta_length[0])
                if progress:
                    print(" Downloading: {0} Bytes: {1}".format(filename, file_size))

                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)

                    status = "{0:16}".format(file_size_dl)
                    if file_size:
                        status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                    status += chr(13)
                    if progress:
                        print(status, end="")
                if progress:
                    print()

        except Exception as e:
            raise

        self.last = filename
        return filename



class DataLoader(object):
    """Class to load program data."""

    def __init__(self, conf, mode='local', path=''):
        self.mode = mode
        self.path = path
        self.dld = DataDownload(path, conf.get('url-prefix', ''))


    def load_data(self, fpath):
        """Load locar or remote data."""
        if self.mode == 'local':
            return self.load_local(fpath)
        elif self.mode == 'remote':
            return self.load_local(self.load_remote(fpath))


    def load_local(self, dataf):
        """Load local data."""
        dt = None
        with open(os.path.join(self.path, dataf), 'r', encoding='utf-8') as l:
            dt = l.read()
        del l
        return dt


    def load_remote(self, dataf):
        """Load remote data."""
        return self.dld.download(dataf, dataf)


    def load_list(self, fpath):
        """Load and parse data using linebreak."""
        return self.load_data(fpath).split('\n')


    def load_yml(self, fpath):
        """Load and parse data to yaml."""
        return yaml.load(self.load_data(fpath))



if __name__ == '__main__':
    import sys

    ddl = DataDownload('temp')
    ddl.download(sys.argv[1], sys.argv[2])
