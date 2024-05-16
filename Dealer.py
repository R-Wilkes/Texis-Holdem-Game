from treys import Card, Evaluator

# this is the class for each perosn to play texis holem
class Dealer:

    def __init__(self, name, deck, board):
        self.name = name
        self.deck = deck
        self.board = []
    
    # Deals cards to people
    def dealCards(self):
        return [self.deck.draw(1)[0] for _ in range(2)]

    # Starts the game
    def startGame(self):
        preDeck = [self.deck.draw(1)[0] for _ in range(3)]
        self.board = [Card.int_to_pretty_str(card) for card in preDeck]

    # Moves to the next player
    def nextTurn(self, player, bot1, bot2):

        # If the player has not folded
        if player.folded == False:

            if player.isTurn == True:

                bot1.isTurn = True
                player.isTurn = False

            elif bot1.isTurn == True:
                
                bot2.isTurn = True
                bot1.isTurn = False

            elif bot2.isTurn == True:
                
                player.isTurn = True
                bot2.isTurn = False

        # If the player has folded
        else:

            if player.isTurn == True:

                bot1.isTurn = True
                player.isTurn = False

            elif bot1.isTurn == True:
                
                bot2.isTurn = True
                bot1.isTurn = False

            elif bot2.isTurn == True:

                bot1.isTurn = True
                bot2.isTurn = False

        

    

    



    



