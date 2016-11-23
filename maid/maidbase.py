
import discord
import asyncio
import time
from random import randint
from .states import State
from .reminders import *


class Maid(object):

    def __init__(self, bot, conf, lobby=None, log=None):
        self.state = State(bot)
        self.start_t = time.time()
        self.bot = bot
        self.conf = conf
        self.lobby = lobby
        self.log = log
        
        self.motivate_list = self.load_list('motivacionais')
        self.presence_list = self.load_list('atividades')
        self.reminder_dict = self.load_yml('lembretes')
        self.reminder_list = list()

        for dayk in self.reminder_dict.keys():
            for hourk in self.reminder_dict[dayk].keys():
                for rem in self.reminder_dict[dayk][hourk]:
                    self.reminder_list.append(Reminder(dayk, hourk, rem))
        self.reminder = ReminderTask(self.conf['tempo']['lembretes'], self.reminder_list, 3)


    def load_data(self, lst):
        dt = None
        with open(self.conf['listas'][lst], 'r', encoding='utf-8') as l:
            dt = l.read()
        del lst
        return dt
    
    def load_list(self, fi):
        return self.load_data(fi).split('\n')
    
    def load_yml(self, fi):
        return yaml.load(self.load_data(fi))

    async def debug(self, msg):
        print(msg)
        if self.log is not None:
            await self.say(self.log, msg, False)

    def uptime(self):
        return divmod(abs(time.time() - self.start_t), 60)

    
    async def go_home(self):
        await self.state.set_state('off')
        await self.play_game(None)

    
    async def start_jobs(self):
        await self.state.set_state('on')
    

    def get_jobs(self):
        return (
            self._motivate_work,
            self._update_presence,
            self._check_reminders
        )

    async def say(self, chan, msg, wait=True):
        if self.state != 'off':
            await self.bot.send_typing(chan)
            if wait:
                await asyncio.sleep(4)
            await self.bot.send_message(chan, msg)


    async def motivate(self, msg):
        if self.lobby is not None:
            await self.say(self.lobby, msg)

    
    async def play_game(self, game_=None):
        if game_ is None:
            self.bot.change_presence(game=None)
        else:
            await self.bot.change_presence(game=discord.Game(name=game_))
    
    async def _check_reminders(self):
        await self.reminder.reminder_task(self._reminder_callback)
    
    async def _reminder_callback(self, rem):
        await self.motivate(rem.msg)


    async def _motivate_work(self):
        await self.bot.wait_until_ready()
        counter = 0
        last_index = -1
        index = -1
        while not self.bot.is_closed:
            await self.debug("Work ping %s" % counter)
            await self.debug("```py\nUP_TIME: {0}min, {1}s\n```".format(*self.uptime()))
            await self.debug(self.lobby)

            if self.lobby is not None and self.state != 'off':
                while last_index == index:
                    index = randint(0, len(self.motivate_list)-1 )
                last_index = index

                msg = self.motivate_list[index]
                await self.motivate(msg)
                counter += 1
            await asyncio.sleep(60*self.conf['tempo']['frases'])
    

    async def _update_presence(self):
        await self.bot.wait_until_ready()
        counter = 0
        last_index = -1
        index = -1
        while not self.bot.is_closed:
            await self.debug("Presence ping %s" % counter)
            await self.debug("```py\nUP_TIME: {0}min, {1}s\n```".format(*self.uptime()))

            if self.state != 'off':
                while last_index == index:
                    index = randint(0, len(self.presence_list)-1 )
                last_index = index

                game = self.presence_list[index]
                await self.play_game(game)
                counter += 1

            await asyncio.sleep(60*self.conf['tempo']['atividade'])