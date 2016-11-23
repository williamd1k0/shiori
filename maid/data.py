
import sys, os, tempfile, logging
from urllib import request, parse


class DataDownload(object):


    def __init__(self, path, url_prefix=''):
        if not os.path.isdir(path):
            os.makedirs(path)
        self.data_path = path
        self.prefix = url_prefix
        self.last = None


    def download(self, url, desc=None, progress=True):
        try:
            u = request.urlopen(url)

            scheme, netloc, path, query, fragment = parse.urlsplit(url)
            filename = os.path.basename(path)
            if not filename:
                filename = 'downloaded.file'
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
                    print(" Downloading: {0} Bytes: {1}".format(desc, file_size))

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
    pass


if __name__ == '__main__':
    
    ddl = DataDownload('temp')
    ddl.download(sys.argv[1], sys.argv[2])