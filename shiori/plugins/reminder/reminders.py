
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
        self.x = x
        self.reminders = dict()
        for rem in rlist:
            if not rem.week in self.reminders:
                self.reminders[rem.week] = []
            self.reminders[rem.week].append(rem)


    def has_reminder_today(self):
        if date.today().isoweekday() in self.reminders:
            return True
        return False

    
    def get_reminders_today(self):
        return self.reminders[date.today().isoweekday()]


    def has_reminder_now(self):
        for rem in self.get_reminders_today():
            if rem.hour <= datetime.today().hour:
                return True
        return False


    def get_reminders_now(self):
        for rem in self.get_reminders_today():
            if rem.hour <= datetime.today().hour:
                yield rem


    async def reminder_task(self, callback):
        while not self.stop:
            if self.has_reminder_today():
                if self.has_reminder_now():
                    for rem in self.get_reminders_now():
                        if rem.x <= self.x:
                            rem.x += 1
                            await callback(rem)
            await asyncio.sleep(60*self.time)
        print('Reminder Done')
