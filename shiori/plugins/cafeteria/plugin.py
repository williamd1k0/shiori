
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
from .products import Coffee
from .products import ProductManager


class CafeteriaPlugin(Plugin):


    def __init__(self, maid):
        super().__init__(maid, 'cafeteria', ['message'])
        self.needs_reload = False
        self.manager = ProductManager()


    async def _product_callback(self, product, message):
        if product.is_empty():
            await self.maid.say(message.channel, product.buy.format(name=product, user=message.author.mention))
            await self.maid.send_typing(message.channel)
            await asyncio.sleep(5)
            product.make()
        await asyncio.sleep(5)
        product.consume_one()
        await self.maid.say(message.channel, product.done.format(name=product, user=message.author.mention))


    def load(self):
        self.manager.add_product(Coffee("cafe com leite", 1.0, ["cafe com leite", "café com leite", "milky coffee"]))
        self.manager.add_product(Coffee("cafe preto", 1.2, ["cafe preto", "café preto", "black coffee"]))
        self.manager.add_product(Coffee('cafe', 1.2, ["cafe", "café", "coffee"]))


    async def mention_callback(self, message):
        await self.message_callback(message)


    async def message_callback(self, message):
        for product in self.manager.products:
            if self.manager.check_order(product, message.content):
                await self._product_callback(self.manager.products[product], message)
                break
