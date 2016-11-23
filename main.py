#!py -3.5

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

import sys
import time
import os.path
import asyncio
import discord
import maid
import yaml
import argparse

parser = argparse.ArgumentParser(prog="Shiori", description="")
parser.add_argument("-r","--remote", help="fetch remote data", action="store_true")
parser.add_argument("-p","--path", metavar="data_path", help="path for data files")
parser.add_argument("-u","--urlprefix", metavar="url", help="prefix domain for data")
parser.add_argument("-v","--version", help="show version", action="store_true")
args = parser.parse_args()

DATA = args.path
CONF = None
REM = None
CONF_F = 'configs.yml'
MODE = 'local'

if args.version:
    print(maid.get_info())
    sys.exit(0)

if args.remote:
    MODE = 'remote'
    REM = maid.DataDownload(DATA, args.urlprefix)
    CONF_F = REM.download(CONF_F)

with open(os.path.join(DATA, CONF_F), 'r') as cf:
    CONF = yaml.load(cf.read())
del cf
CONF['url-prefix'] = args.urlprefix


coffee = maid.Coffee("café preto", 1.5, ["quero cafe", "quero café", "gimme coffee"])


maid.Command('init', 
    [
    'bom trabalho',
    '!init'
    ], 'Muito obrigada.')

maid.Command('log', 
    [
    'jogue o lixo aqui',
    '!log'
    ], 'Tudo bem.')

maid.Command('bye', 
    [
    'esta liberada',
    'está liberada',
    '!bye'
    ], 'Muito obrigada. Até amanhã.')



bot = discord.Client()

shiori = maid.Maid(bot, CONF, maid.DataLoader(CONF, MODE, DATA))


@bot.event
async def on_ready():
    await shiori.debug('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
    await shiori.state.set_state('away')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        await shiori.debug("Mention Check")
        cmd = maid.Command.search(message.content)
        if cmd is not None:
            if cmd.name == 'init':
                shiori.lobby = message.channel
                await shiori.debug(shiori.lobby)
                await shiori.start_jobs()
                await shiori.say(message.channel, cmd.msg)
            elif cmd.name == 'log':
                shiori.log = message.channel
                await shiori.debug(shiori.log)
                await shiori.say(message.channel, cmd.msg)
                
                if 'lobby' in CONF['discord']:
                    shiori.lobby = message.server.get_channel(str(CONF['discord']['lobby']))
                    await shiori.debug(shiori.lobby)
                    await shiori.start_jobs()

            elif cmd.name == 'bye':
                await shiori.say(message.channel, cmd.msg)
                await shiori.go_home()

        else:
            msg = 'Alguém me chamou? Como posso ser útil?'.format(message)
            await bot.send_message(message.channel, msg)

    for term in coffee.terms:
        if term in message.content:
            if coffee.is_empty():
                msg = 'Já vou preparar, {0.author.mention}'.format(message)
                time.sleep(5)
                await bot.send_message(message.channel, msg)
                coffee.make()
            
            time.sleep(5)
            coffee.consume()
            msg = 'Aqui está o seu '+coffee.name+', {0.author.mention} :coffee:'.format(message)
            await bot.send_message(message.channel, msg)
            break


@bot.event
async def on_message_edit(before, after):
    pass
    #msg = "Eu vi o que você fez aí, {0.author.mention}!".format(after)
    #await bot.send_message(after.channel, msg)


def shut_down(er):
    print("Estou morrendo :scream:")
    print("```shell\n{0}\n```".format(er))
    bot.close()

try:
    for job in shiori.get_jobs():
        bot.loop.create_task(job())
        
    bot.run(CONF['discord']['token'])

except Exception as er:
    shut_down(er)
