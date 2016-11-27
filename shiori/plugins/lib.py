
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

import asyncio
import time

class Plugin(object):
    """Base class for all plugins."""

    def __init__(self, maid, name, types):
        self.data = None
        if name in maid.conf['plugins']:
            self.data = maid.conf['plugins'][name]
        self.tasks = []
        self.maid = maid
        self.name = name
        self.types = types
        self.needs_reload = True
        self.mode = True
        self.interval = 1


    def __repr__(self):
        return '<Plugin:{0}>'.format(self.name)

    def __str__(self):
        return repr(self)


    def load(self):
        """Abstract load plugin."""
        pass


    def _load(self):
        """Load backend"""
        print('LOADING {0}'.format(self))
        init = time.time()
        self.load()
        print('LOADED {0} in {1}s'.format(self, time.time()-init))


    def update_data(self):
        """Abstract update data files of plugin."""
        pass


    async def new_task(self):
        """Abstract create new task for plugin."""
        pass


    async def loop_callback(self):
        """Abstract callback for loop plugins."""
        pass


    async def mention_callback(self, message):
        """Abstract callback for mention plugins."""
        pass


class PluginManager(object):


    def __init__(self, plugins, auto_load=True):
        self.plugins = plugins
        if auto_load:
            self.load()


    def load(self):
        for pl in self.plugins:
            if not issubclass(pl.__class__, Plugin):
                raise NotAPluginException()
            pl._load()


    def update_data(self):
        for pl in self.plugins:
            print('Updating {0}'.format(pl))
            if pl.needs_reload:
                pl.update_data()


    def get_job_plugins(self):
        jobs = []
        for pl in self.plugins:
            if pl.mode:
                if 'loop' in pl.types:
                    jobs.append(pl)
        return jobs


    def get_mentions(self):
        cmds = []
        for pl in self.plugins:
            if pl.mode:
                if 'mention' in pl.types:
                    cmds.append(pl.mention_callback)
        return cmds


    def get_commands(self):
        pass


class NotAPluginException(Exception):
    pass


class CmdTool(object):

    def __init__(self, maid, prefix='', case_sensitive=False):
        self.maid = maid
        self.prefix = prefix
        self.case_sensitive = case_sensitive


    def has_command(self, cmd, msg):
        if self.case_sensitive:
            return self.prefix+cmd in msg.content
        else:
            return (self.prefix+cmd).lower() in msg.content.lower()
    
    def has_commands(self, cmds, msg):
        for cmd in cmds:
            if self.has_command(cmd, msg):
                return True
        return False