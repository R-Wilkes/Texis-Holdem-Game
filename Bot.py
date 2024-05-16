from treys import Card
# this is the class for each perosn to play texis holem
class Bot:

    def __init__(self, name, startingMoney, cards):
        self.name = name
        self.money = startingMoney
        self.cards = cards
        self.isTurn = False

    def bet(self, amount):
        if amount > self.money:
            return False
        
        else:

            self.money -= amount
            return True
        
    def check(self):
        return True

    def fold(self, currentBet):
        if currentBet > self.money:

            return True
        
        else:

            return False

    def getCards(self):
        return [Card.int_to_pretty_str(card) for card in self.cards]

