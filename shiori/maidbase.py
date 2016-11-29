
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

import time
import asyncio
import discord
from .utils import code_block
from .states import State
from .plugins import CmdTool, PluginManager, instance_all_plugins


class Maid(discord.Client):


    def __init__(self, conf, loader, lobby=None, log=None):
        super().__init__()
        self.bot = self # deprecated/legacy bot instance
        self.state = State(self)
        self.start_t = time.time()
        self.conf = conf
        self.loader = loader
        self.lobby = lobby
        self.log = log

        self.cmdtool = CmdTool('!')
        self.plugins = PluginManager(list(instance_all_plugins(self)))


    """
     * Client Events
    """
    async def on_ready(self):
        await self.debug('Logged in as:\n{0} (ID: {0.id})'.format(self.user))
        await self.state.set_state('away')
        

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            for mention in self.plugins.get_mentions():
                await mention.mention_callback(message)

        else:
            for message_plugin in self.plugins.get_messages():
                await message_plugin.message_callback(message)


    async def debug(self, msg):
        print(msg)
        if self.log is not None:
            await self.say(self.log, code_block(msg, 'yaml'), False)


    def uptime(self):
        return divmod(abs(time.time() - self.start_t), 60)


    async def go_home(self):
        await self.state.set_state('off')
        await self.play_game(None)


    async def start_jobs(self):
        await self.state.set_state('on')


    def get_job_plugins(self):
        return self.plugins.get_job_plugins()


    def create_tasks(self):
        for job in self.get_job_plugins():
            job.tasks.append(self.loop.create_task(job.loop_callback()))


    async def say(self, chan, msg, wait=True):
        if self.state != 'off':
            await self.bot.send_typing(chan)
            if wait:
                await asyncio.sleep(1)
            await self.bot.send_message(chan, msg)


    async def motivate(self, msg):
        if self.lobby is not None:
            await self.say(self.lobby, msg)


    async def play_game(self, game_=None):
        if game_ is None:
            self.bot.change_presence(game=None)
        else:
            await self.bot.change_presence(game=discord.Game(name=game_))
