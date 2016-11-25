
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
import wikipedia
from ...utils import code_block 
from ...plugins import Plugin

class WikiPlugin(Plugin):

    page = None

    def __init__(self, maid):
        super().__init__(maid, 'wiki', ['loop'])


    def load(self):
        print(self.data)
        self.mode = self.data.get('mode', False)
        self.interval = self.data.get('interval', 60)
        wikipedia.set_lang("pt")
        print('loaded')

    def update_data(self):
        self.load()


    async def loop_callback(self):
        await self.maid.wait_until_ready()
        counter = 0
        print(self.mode)
        while not self.maid.is_closed and self.mode:
            await self.maid.debug("Wiki ping %s" % counter)
            await self.maid.debug("UP_TIME: {0}min, {1}s".format(*self.maid.uptime()))
            if self.maid.lobby is not None and self.maid.state != 'off':
                self.page = wikipedia.page(wikipedia.random())
                await self.maid.motivate(code_block(self.page.summary))
                counter += 1
            await asyncio.sleep(60*self.interval)
    