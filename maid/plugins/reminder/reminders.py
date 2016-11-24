
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
from datetime import date
from datetime import datetime


class Reminder(object):

    def __init__(self, week, hour, msg):
        self.week = week
        self.hour = hour
        self.msg = msg
        self.x = 0


class ReminderTask(object):

    def __init__(self, time, rlist, x=1):
        self.stop = False
        self.time = time
        self.reminders = None
        self.now = None
        self.x = x
        self.rdict = dict()
        for rem in rlist:
            if not rem.week in self.rdict:
                self.rdict[rem.week] = []
            self.rdict[rem.week].append(rem)
    
    def has_reminder_today(self):
        if date.today().isoweekday() in self.rdict:
            self.reminders = self.rdict[date.today().isoweekday()]
            return True
        return False

    def has_reminder_now(self):
        now = []
        for rem in self.reminders:
            if rem.hour <= datetime.today().hour:
                now.append(rem)
        self.now = now
        if len(now) > 0:
            return True
        return False

    async def reminder_task(self, callback):
        while not self.stop:
            if self.has_reminder_today():
                if self.has_reminder_now():
                    for rem in self.now:
                        if rem.x <= self.x:
                            rem.x += 1
                            await callback(rem)
            await asyncio.sleep(60*self.time)
        print('Reminder Done')
        
    