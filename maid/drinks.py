

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
    