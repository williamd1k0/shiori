
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

import os
import subprocess
from ...plugins import Plugin


class GitRepo(object):

    def __init__(self, path, remote, branch='master'):
        self.path = os.path.abspath(path)
        self.remote = remote
        self.branch = branch
        self.init_check()

    def init_check(self):
        if not os.path.isdir(self.path):
            self.clone()
        else:
            self.fetch()
        self.checkout(self.branch)

    def clone(self):
        cmd = 'git', 'clone', self.remote, self.path
        subprocess.call(cmd)

    def fetch(self):
        cmd = 'cd', self.path, '&&'
        cmd += 'git', 'fetch', 'origin'
        subprocess.call(cmd, shell=True)

    def checkout(self, branch):
        cmd = 'cd', self.path, '&&'
        cmd += 'git', 'checkout', branch
        subprocess.call(cmd, shell=True)
        self.branch = branch

    def zip_branch(self, path=None, branch=None):
        if branch is None:
            branch = self.branch
        path = os.path.join(self.path, '.git', branch+'.zip')
        cmd = 'cd', self.path, '&&'
        cmd += 'git', 'archive', '--format', 'zip', '--output', path, branch
        subprocess.call(cmd, shell=True)
        return path


class GitRepoPlugin(Plugin):

    terms = None
    msg = None

    def __init__(self, maid):
        super().__init__(maid, 'gitrepo', ['mention'])
        self.needs_reload = False
        self.terms = {}
        self.msg = {}
        self.callbacks = {}


    async def _repo_callback(self, message):
        msg_list = message.content.split(' ')[2:]
        if len(msg_list) > 0:
            remote = self.data['repos'][msg_list[0]]['remote']
            path = self.data['repos'][msg_list[0]]['path']
            branch = 'master'
            if len(msg_list) > 1:
                branch = msg_list[1]
            await self.maid.say(message.channel, 'Checking repo...')
            repo = GitRepo(path, remote, branch)
            await self.maid.say(message.channel, 'Uploading repo...')
            zip_file = repo.zip_branch()
            await self.maid.send_file(message.channel, zip_file)


    def load(self):
        self.terms['repo'] = 'repo', 'git'
        self.msg['repo'] = 'Uploaded successfully.'
        self.callbacks['repo'] = self._repo_callback


    async def mention_callback(self, message):
        for term in self.terms:
            if self.maid.cmdtool.has_commands(self.terms[term], message):
                await self.callbacks[term](message)
                await self.maid.say(message.channel, self.msg[term].format(message))
