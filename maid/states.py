
import discord
import asyncio


class State(object):

    # States
    STATE_ON    = 0
    STATE_AWAY  = 1
    STATE_BUSY  = 2
    STATE_OFF   = 3

    STATES = {
        'on':STATE_ON,
        'away':STATE_AWAY,
        'busy':STATE_BUSY,
        'off':STATE_OFF
    }

    D_STATES = [
        discord.Status.online,
        discord.Status.idle,
        discord.Status.dnd,
        discord.Status.offline
    ]

    def __init__(self, client, start=0):
        self.state = start
        self.client = client

    async def set_state(self, st):
        if type(st) is str:
            self.state = self.STATES[st]
        elif type(st) is int:
            self.state = st
        await self.client.change_presence(status=self.D_STATES[self.state])

    def __eq__(self, st):
        return self.STATES[st] == self.state
    
    def __ne__(self, st):
        return not self.__eq__(st)