from treys import Card
# this is the class for each perosn to play texis holem
class Person:

    def __init__(self, name, startingMoney, cards):
        self.name = name
        self.money = startingMoney
        self.cards = cards
        self.isTurn = True
        self.folded = False

    # Will take the amount and subtract it from the money if there is enough
    def bet(self, amount):
        if amount > self.money:
            return False
        
        else:

            self.money -= amount
            return True
        
    def check(self):
        return True

    # Folds your hand
    def fold(self):
    
        self.folded = True


    def getCards(self):
        return [Card.int_to_pretty_str(card) for card in self.cards]

