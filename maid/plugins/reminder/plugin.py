
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
from .reminders import * 

class ReminderPlugin(Plugin):

    reminder_dict = None
    reminder_list = None
    reminder = None

    def __init__(self, maid):
        super().__init__(maid, 'reminder', 'loop')


    def load(self):
        self.reminder_dict = self.maid.loader.load_yml('lembretes')
        self.reminder_list = list()

        for dayk in self.reminder_dict.keys():
            for hourk in self.reminder_dict[dayk].keys():
                for rem in self.reminder_dict[dayk][hourk]:
                    self.reminder_list.append(Reminder(dayk, hourk, rem))
        self.reminder = ReminderTask(self.maid.conf['tempo']['lembretes'], self.reminder_list, 3)
        print(self.reminder_list)

    async def loop_callback(self):
        await self.reminder.reminder_task(self._reminder_callback)
    
    async def _reminder_callback(self, rem):
        await self.maid.motivate(rem.msg)