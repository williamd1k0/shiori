
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

from ...plugins import Plugin


class CommandsPlugin(Plugin):

    terms = None
    msg = None

    def __init__(self, maid):
        super().__init__(maid, 'debug', ['mention'])
        self.needs_reload = False
        self.terms = {}
        self.msg = {}
        self.callbacks = {}


    async def _debug_callback(self, message):
        self.maid.log = message.channel
        await self.debug(self.maid.log)
        if 'lobby' in self.maid.conf['discord']:
            await self._init_callback(message)


    async def _init_callback(self, message):
        if 'lobby' in self.maid.conf['discord']:
            self.maid.lobby = message.server.get_channel(str(self.maid.conf['discord']['lobby']))
        else:
            self.maid.lobby = message.channel
        await self.debug(self.maid.lobby)
        await self.maid.start_jobs()


    async def _sleep_callback(self, message):
        await self.maid.say(message.channel, self.msg['sleep'].format(message))
        await self.maid.go_home()


    async def _backup_callback(self, message):
        self.maid.data.backup_data()
        await self.maid.send_file(message.channel, self.maid.data.backup.last_backup)


    def load(self):
        self.terms['debug'] = 'log', 'debug'
        self.msg['debug'] = 'Jogando o lixo em `{0.channel}`'
        self.callbacks['debug'] = self._debug_callback

        self.terms['init'] = 'init', 'start', 'work'
        self.msg['init'] = 'Iniciando trabalhos em {0.channel}'
        self.callbacks['init'] = self._init_callback

        self.terms['sleep'] = 'bye', 'stop', 'sleep'
        self.msg['sleep'] = 'Tchau, até amanhã {0.author.mention}'
        self.callbacks['sleep'] = self._sleep_callback

        self.terms['backup'] = 'backup', 'save'
        self.msg['backup'] = '{0.author.mention}, aqui está seu backup!'
        self.callbacks['backup'] = self._backup_callback


    async def mention_callback(self, message):
        for term in self.terms:
            if self.maid.cmdtool.has_commands(self.terms[term], message):
                await self.callbacks[term](message)
                await self.maid.say(message.channel, self.msg[term].format(message))
