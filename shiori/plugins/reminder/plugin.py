
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
from ...plugins import Plugin
from .reminders import * 

class ReminderPlugin(Plugin):


    reminder_dict = None
    reminder_list = None
    reminders = None


    def __init__(self, maid):
        super().__init__(maid, 'reminder', ['loop'])
        self.reminders = []


    def load(self):
        self.mode = self.data.get('mode', False)
        self.interval = self.data.get('interval', 30)
        self.reminder_dict = self.maid.loader.load_yml(self.data.get('data'))
        self.reminder_list = list()

        for dayk in self.reminder_dict.keys():
            for hourk in self.reminder_dict[dayk].keys():
                for rem in self.reminder_dict[dayk][hourk]:
                    self.reminder_list.append(Reminder(dayk, hourk, rem))
        self.reminders.append(ReminderTask(self.interval, self.reminder_list, 3))


    def update_data(self):
        self.reminders[-1].stop = True
        self.load()
        self.tasks.append(self.maid.loop.create_task(self.loop_callback()))


    async def new_task(self):
        print("Starting new task")
        while not self.tasks[-1].done():
            print('Waiting for {0}'.format(self.tasks[-1]))
            await asyncio.sleep(60)
        self.load()
        self.tasks.append(self.maid.loop.create_task(self.loop_callback()))


    async def loop_callback(self):
        await self.reminders[-1].reminder_task(self._reminder_callback)


    async def _reminder_callback(self, rem):
        await self.maid.motivate(rem.msg)
        