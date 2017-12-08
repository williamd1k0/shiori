
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

from . import badwords
from ...plugins import Plugin


class BadWordsPlugin(Plugin):

    terms = ['badword', 'badwords']
    msg = None
    re = None

    def __init__(self, maid):
        super().__init__(maid, 'badwords', ['mention'])
        self.needs_reload = False

    def load(self):
        self.re = badwords.load_patterns()
        print("Badwords loaded.")

    async def mention_callback(self, message):
        for term in self.terms:
            if self.maid.cmdtool.has_command(term, message):
                words = badwords.get_badwords(self.re, message.content.replace(term, ''))
                if words:
                    await self.maid.say(message.channel, 'Text contains bad words :rage::underage:')
                else:
                    await self.maid.say(message.channel, 'Text is safe :angel:')
                break
