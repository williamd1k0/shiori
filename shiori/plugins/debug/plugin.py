
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


class DebugPlugin(Plugin):

    terms = None
    msg = None

    def __init__(self, maid):
        super().__init__(maid, 'debug', 'mention')
        self.needs_reload = False

    def load(self):
        self.terms = ['log', 'debug']
        self.msg = 'Jogando o lixo em {0}'


    async def mention_callback(self, message):
        if self.maid.cmdtool.has_commands(self.terms, message):
            self.maid.log = message.channel
            await self.maid.debug(self.maid.log)
            await self.maid.say(message.channel, self.msg.format(message.channel))

            if 'lobby' in self.maid.conf['discord']:
                self.maid.lobby = message.server.get_channel(str(self.maid.conf['discord']['lobby']))
                await self.maid.debug(self.maid.lobby)
                await self.maid.start_jobs()