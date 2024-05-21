from treys import Card
# this is the class for each perosn to play texis holem
class Person:

    def __init__(self, name, startingMoney, cards):

        self.name = name
        self.money = startingMoney
        self.cards = cards
        self.isTurn = True
        self.folded = False
        self.allIn = False
        self.matchedBet = 0


    # Will take the amount and subtract it from the money if there is enough
    def bet(self, amount):

        if amount > self.money:
            return False
        
        else:

            self.money -= amount
            self.matchedBet = amount
            return True
        
    def check(self):
        return True
    
    # Folds your hand
    def fold(self):
        self.folded = True

    # Gets the pretty string of the card
    def getCards(self):
        return [Card.int_to_pretty_str(card) for card in self.cards]
    
    # Gets the int value of the cards
    def getCardsInt(self):
        return self.cards

    # This will display the option of moves
    def getOptions(self, dealer):

        if dealer.currentBet == 0:
            return "Check, Bet or Fold? "
        
        elif dealer.currentBet > self.money:
            return "All in or Fold? "
        
        elif dealer.currentBet <= self.money:
            return "Call, Raise or Fold? "
