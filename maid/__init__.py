
from .data import *
from .states import State
from .maidbase import Maid
from .drinks import *
from .commands import Command

__app__     = "Shiori"
__author__  = "William Tumeo"
__version__ = 0, 7, 2

def get_info():
    return "{0} v{1}.{2}.{3} by {4}".format(__app__, *__version__, __author__)
