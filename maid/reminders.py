
import yaml
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
        print(self.reminders)
        for rem in self.reminders:
            print(rem)
            if rem.hour <= datetime.today().hour:
                now.append(rem)
        self.now = now
        if len(now) > 0:
            return True
        return False

    async def reminder_task(self, callback):
        while True:
            if self.has_reminder_today():
                if self.has_reminder_now():
                    for rem in self.now:
                        if rem.x <= self.x:
                            rem.x += 1
                            await callback(rem)
            await asyncio.sleep(60*self.time)
        
    