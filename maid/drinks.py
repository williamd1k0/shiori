
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

class Drink(object):

    def __init__( self, name, full, terms, quantity=0 ):
        self.name = name
        self.full = full
        self.quantity = quantity
        self.terms = terms
    
    def consume(self):
        pass
    
    def is_empty(self):
        return self.quantity <= 0

    def is_full(self):
        return self.quantity >= self.full
    
    def make(self):
        self.quantity = self.full


class Coffee(Drink):

    def consume(self):
        self.quantity -= 0.2

if __name__ == '__main__':
    coffee = Coffee("café preto", 1.5, ["quero cafe", "quero café", "gimme coffee"])
