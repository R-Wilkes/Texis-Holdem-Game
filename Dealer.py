from treys import Card, Evaluator
import random
from time import sleep

# Straight Flush: The best possible hand, scores in the range of 1 to 10.
# Four of a Kind: Scores in the range of 11 to 166.
# Full House: Scores in the range of 167 to 322.
# Flush: Scores in the range of 323 to 1599.
# Straight: Scores in the range of 1600 to 1609.
# Three of a Kind: Scores in the range of 1610 to 2467.
# Two Pair: Scores in the range of 2468 to 3325.
# One Pair: Scores in the range of 3326 to 6185.
# High Card: Scores in the range of 6186 to 7462.

# this is the class for each perosn to play texis holem
class Dealer:

    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.board = []
        self.pot = 0
        self.currentBet = 0
        self.canCheck = True
        self.evaluator = Evaluator()
        self.cheats = False
        self.difficlutyChoice = None
    
    # Changes the check
    def changeCheck(self):

        if self.currentBet != 0:
            self.canCheck = False
        
        else:
            self.canCheck = True

    # Deals cards to people
    def dealCards(self):
        return [self.deck.draw(1)[0] for _ in range(2)]

    # Gets the board
    def getBoard(self):
        return [Card.int_to_pretty_str(card) for card in self.board]
    
    # Starts the game
    def startGame(self):
        self.board = [self.deck.draw(1)[0] for _ in range(3)]

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

    # Returns the score of the hand
    def getScore(self, hand):
        
        evaluator = Evaluator()
        return evaluator.evaluate(hand, self.board)

    # Will add a new card to the board
    def drawCard(self):
        self.board.append(self.deck.draw(1)[0])

    # Will check if the bets are matched
    def betsMatched(self, player, bot1, bot2):

        players = [player, bot1, bot2]
        active_players = [p for p in players if not p.folded]
        matched_players = [p for p in active_players if p.matchedBet == self.currentBet]

        if all(p.matchedBet == self.currentBet for p in active_players):

            # print("All players matched the bet.")
            return True
        
        else:

            # print("The following players matched the bet:")

            for player in matched_players:
                # print(player.name)
                pass

            return False
    
    # Returns the amount of players
    def amountIn(self, player, bot1, bot2):

        active_players = [player, bot1, bot2]
        count = 0
        for p in active_players:
            if not p.folded:
                count += 1
        return count

    # Will return the winner
    def getWinner(self, player, bot1, bot2):

        players = [player, bot1, bot2]
        active_players = [p for p in players if not p.folded]
        scores = [self.getScore(p.cards) for p in active_players]
        max_score = max(scores)
        winners = [p for p, s in zip(active_players, scores) if s == max_score]
        return winners

    # will reset the round, reset all the temp varibles
    def resetRound(self, player, bot1, bot2):
            
            player.isTurn = True
            bot1.isTurn = False
            bot2.isTurn = False
            player.matchedBet = 0
            bot1.matchedBet = 0
            bot2.matchedBet = 0
            self.currentBet = 0
            self.canCheck = True
    
    # will reset the game after it is over
    def resetGame(self, player, bot1, bot2):

        self.pot = 0
        self.board = []
        self.currentBet = 0
        self.canCheck = True
        self.resetRound(player, bot1, bot2)
        self.startGame()
        player.cars = self.dealCards()
        bot1.cards = self.dealCards()
        bot2.cards = self.dealCards()
        bot1.folded = False
        bot2.folded = False
        player.folded = False
        bot1.allIn = False
        bot2.allIn = False
        player.allIn = False

    # Will return the class of the cards
    def cardClass(self, card):

        score = self.evaluator.evaluate(card, self.board)
        hand_class = self.evaluator.get_rank_class(score)

        return self.evaluator.class_to_string(hand_class)

    # Will make the difficulyt of the bots
    def difficultyDecider(self):
            
        if self.difficlutyChoice == None:

            while True:
                choice = input("Choose Difficulty: Easy, Impossible, Cheater, Random? ")

                if (choice.lower()).strip() == "easy" or self.difficlutyChoice == "easy":

                    print("WIMP")
                    sleep(3)
                    self.difficlutyChoice = "easy"
                    return random.uniform(1.1, 1.9)
                
                elif (choice.lower()).strip() == "cheater" or self.difficlutyChoice == "cheater":
                        
                        print("Good Luck! Your gonna need it :)")
                        sleep(3)
                        self.difficlutyChoice = "cheater"
                        return 5
                
                elif (choice.lower()).strip() == "random" or self.difficlutyChoice == "random":
                        
                    print("Good Luck!")
                    sleep(3)
                    self.difficlutyChoice = "random"
                    return random.uniform(1.1, 3.5)

                elif (choice.lower()).strip() == "impossible" or self.difficlutyChoice == "impossible":

                    print("Feeling Lucky???")
                    sleep(3)
                    self.difficlutyChoice = "impossible"
                    return 4

                else:
                    print("Invalid Choice")
       
        else:

            if self.difficlutyChoice == "easy":

                self.difficlutyChoice = "easy"
                return random.uniform(1.1, 1.9)
            
            elif self.difficlutyChoice == "cheater":
                    
                    self.difficlutyChoice = "cheater"
                    return 4
            
            elif self.difficlutyChoice == "random":
                        
                self.difficlutyChoice = "random"
                return random.uniform(1.1, 3.5)

            elif self.difficlutyChoice == "impossible":

                self.difficlutyChoice = "impossible"
                return 5
