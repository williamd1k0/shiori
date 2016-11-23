
class Command(object):

    __cmds = list()

    def __init__(self, name, terms, msg=None, callback=(lambda x:x)):
        self.name = name
        self.terms = terms
        self.msg = msg
        self.callback = callback
        self.__cmds.append(self)
    
    @classmethod
    def search(cls, text):
        for cmd in cls.__cmds:
            for tm in cmd.terms:
                if tm.lower() in text.lower():
                    return cmd
        return None