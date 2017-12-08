
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

import json
from urllib.request import urlopen
from ...plugins import Plugin


class BitcoinPlugin(Plugin):

    terms = ['bitcoin', 'btc']
    prev = None

    def __init__(self, maid):
        super().__init__(maid, 'bitcoin', ['mention'])
        self.needs_reload = False

    def load(self):
        print("Bitcoin loaded.")

    async def get_bitcoin_price(self):
        data = urlopen('https://api.bitcointrade.com.br/v1/public/BTC/ticker').read()
        btc = float(json.loads(data.decode('utf-8'))['data']['last'])
        msg = "{status} R$ {btc:.2f}{diff}"
        prev = self.prev
        if prev is None:
            msg = msg.format(status='', btc=btc, diff='')
        elif btc > prev:
            msg = msg.format(status=':airplane_departure:', btc=btc, diff=' (+%.2f)' % (btc-prev))
        elif btc < prev:
            msg = msg.format(status=':airplane_arriving:', btc=btc, diff=' (-%.2f)' % (prev-btc))
        else:
            msg = msg.format(status='', btc=btc, diff='')
        self.prev = btc
        return msg

    async def mention_callback(self, message):
        for term in self.terms:
            if self.maid.cmdtool.has_command(term, message):
                await self.maid.say(message.channel, await self.get_bitcoin_price())
                break
