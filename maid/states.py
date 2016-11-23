
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