
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
from ...utils import RandomPick
from ...plugins import Plugin

class PlayingJoojPlugin(Plugin):

    presence_list = None


    def __init__(self, maid):
        super().__init__(maid, 'playingjooj', ['loop'])


    def load(self):
        self.presence_list = RandomPick(self.maid.loader.load_list(self.data.get('data')))


    def update_data(self):
        self.load()


    async def loop_callback(self):
        await self.maid.bot.wait_until_ready()
        counter = 0
        while not self.maid.bot.is_closed and self.mode:
            await self.maid.debug("Presence ping %s" % counter)
            await self.maid.debug("UP_TIME: {0}min, {1}s".format(*self.maid.uptime()))

            if self.maid.state != 'off':
                game = self.presence_list.pick_one()
                await self.maid.play_game(game)
                counter += 1

            await asyncio.sleep(60*self.interval)
    