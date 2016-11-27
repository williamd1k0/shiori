
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


class Product(object):


    def __init__(self, name, full, terms, items,
        quantity=0, unit=['unit', 'units'],
        buy='Vou comprar mais {name}',
        done='Aqui está o seu {name}, {user}'
    ):
        self.name = name
        self.full = full
        self.terms = terms
        self.quantity = quantity
        self.items = items
        self.unit = unit
        self.buy = buy
        self.done = done

    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name


    def consume_one(self):
        pass


    def consume_all(self):
        pass


    def is_empty(self):
        return self.quantity <= 0


    def is_full(self):
        return self.quantity >= self.full


    def make(self):
        self.quantity = self.full


class ProductManager(object):


    def __init__(self):
        self.products = {}


    def add_product(self, product: Product):
        if not product.name in self.products:
            self.products[product.name] = product


    def check_order(self, name, content):
        content = content.lower()
        for context in self.products[name].terms:
            for item in self.products[name].items:
                if '{unit}' in context:
                    for unit in self.products[name].unit:
                        if context.format(unit=unit, item=item) in content:
                            return True
                elif context.format(item=item) in content:
                    return True
        return False


class Drink(Product):


    def __init__(self, name, full, items):
        terms = [
            'quero {item}',
            'quero um {item}',
            'queria {item}',
            'queria um {item}',
            'preciso de {item}',
            'preciso de um {item}',
            'gimme {item}',
            'gimme a {item}',
            'want a {item}',
            'wanna a {item}',
            'tomar {item}',
            'tomar um {item}',
            'uma {unit} de {item}'
        ]
        units = ['xícara', 'xícaras', 'xicara', 'xicaras']
        buy = 'Vou preparar mais {name}, {user}'
        done = 'Aqui está seu {name}, {user}'
        super().__init__(name, full, terms, items, quantity=0, unit=units, buy=buy, done=done)



class Coffee(Drink):


    def consume_one(self):
        self.quantity -= 0.2



if __name__ == '__main__':
    coffee = Coffee("cafe", 1.5, ["cafe", "café", "coffee"])
    coffee_p = Coffee("cafe preto", 1.5, ["cafe preto", "café preto", "black coffee"])
    coffee_l = Coffee("cafe com leite", 1.5, ["cafe com leite", "café com leite", "milky coffee"])
    mg = ProductManager()
    mg.add_product(coffee)
