from treys import Card
import random

# this is the class for each perosn to play texis holem
class Bot:

    def __init__(self, name, startingMoney, cards, difficulty):

        self.name = name
        self.money = startingMoney
        self.cards = cards
        self.isTurn = False
        self.folded = False
        self.allIn = False
        self.difficulty = difficulty
        self.bluffChance = self.calculateBluff()
        self.matchedBet = 0
        
    # This just calculates the bluffing chance
    def calculateBluff(self):
        return (self.difficulty * random.randint(5,20)) + 10

    # Will take the amount and subtract it from the money if there is enough
    def bet(self, amount):

        if amount > self.money:
            return False
        
        else:

            self.money -= amount
            return True
    
    # Will check
    def check(self):
        return "Checking"

    # Folds your hand
    def fold(self, currentBet):
            return True
        

    # Gets the pretty string of the card
    def getCards(self):
        return [Card.int_to_pretty_str(card) for card in self.cards]

    # Gets the int value of the cards
    def getCardsInt(self):
        return self.cards

    # This will determine if the bot will bluff
    def bluff(self, currentBet):

        # Determines if the bot will bluff
        if self.bluffChance > random.randint(0, 100) and currentBet < (self.money - random.randint(0, 100)):
            return True

        else:
            return False

    # Will call the bet
    def call(self, currentBet):

        if currentBet > self.money:
            return False
        
        else:

            self.money -= currentBet
            return True

    # Will go all in
    def allIns(self):

        self.allIn = True

    # The complex method that will decide what the bot will do
    def decideMove(self, dealer, player, bot):

        # Easy Peasy
        if self.difficulty >= 1.1 and self.difficulty <= 1.9:

            # If the bot can bet or check or fold
            if dealer.currentBet == 0:

                # Will see if it can check
                if dealer.canCheck and dealer.getScore(self.cards) > 5000 + random.randint(100, 1000):
                    return self.check()

                # Will bluff
                if self.bluff(dealer.currentBet) and dealer.currentBet != 0:

                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Bluffing but Calling"
                
                # Will Bluff Bet
                elif self.bluff(dealer.currentBet) and dealer.currentBet == 0:
                        
                        betAmount = random.randint(10, random.randint(100, 400))
    
                        if self.bet(betAmount):
    
                            dealer.pot += betAmount
                            dealer.currentBet = betAmount
                            dealer.changeCheck()
                            self.matchedBet = dealer.currentBet
    
                            return "Bluffing but Betted " + str(betAmount)

                # Will have to change the numer thing, will bet
                if dealer.getScore(self.cards) < 6000:
                    
                    # If doing really well, it will bet
                    if dealer.getScore(self.cards) < 3000:
                            
                            betAmount = random.randint(0, self.money)
                            if self.bet(betAmount):
        
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                dealer.changeCheck()
                                self.matchedBet = dealer.currentBet
        
                                return "Betted " + str(betAmount)
                            
                    betAmount = random.randint(10, (200 * self.difficulty + 50))

                    if self.bet(betAmount):

                        dealer.pot += betAmount
                        dealer.currentBet = betAmount
                        dealer.changeCheck()
                        self.matchedBet = dealer.currentBet

                        return "Betted " + str(betAmount)

                # Last resort
                if dealer.canCheck:
                    return self.check() + " Last Resort"
                
                # Will match minor Bets, bc why not
                if dealer.currentBet == 10 or dealer.currentBet == 20 or dealer.currentBet == 30 or dealer.currentBet == 40 or dealer.currentBet == 50:
                    
                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
                
                # Will match bigger bets based on difficulty
                if dealer.currentBet >= 100 and random.randint(0, 100) < self.difficulty * 20 + 10:

                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
                

                # This will fold
                self.folded = True
                return "Folding"
            
            # If it cant bet
            else:

                # Will match the bet 
                if dealer.currentBet != self.matchedBet:

                    # If it can match the current bet
                    if self.call(dealer.currentBet - self.matchedBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Matching Bet"
                    
                    # Will raise the bet if feeling it
                    if (dealer.getScore(self.cards) < 4000 + random.randint(100, 400) - (500 * self.difficulty)) and self.money >= dealer.currentBet:
                            
                            betAmount = random.randint(10, (200 * self.difficulty + 50))
    
                            if self.bet(betAmount):
    
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                self.matchedBet = dealer.currentBet
                                return "Raising Bet " + str(betAmount)
                    
                    # Will go all in if it does not have enough money
                    if (dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (500 * self.difficulty)) and self.money <= (dealer.currentBet - self.matchedBet):

                        self.allIn()
                        self.money = 0
                        return "All In"
                    
                    else:
                        self.folded = True
                        return "Folding"
                
                elif dealer.currentBet == self.matchedBet:

                    return "Already Matched Bet"
                
                # If it can call, it will probably
                if (dealer.getScore(self.cards) < 5000 + random.randint(100, 1500) - (500 * self.difficulty)) and self.money >= dealer.currentBet:

                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
        
                # Will go all in
                if dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (500 * self.difficulty) and self.money <= dealer.currentBet:

                    self.allIn()
                    self.money = 0
                    return "All In"
                
                 # Will fold
                
                else:
                    
                    self.folded = True
                    return "Folding"

        # Mid Difficulty
        elif self.difficulty >= 2 and self.difficulty <= 2.9:
                 # If the bot can bet or check or fold
            if dealer.currentBet == 0:

                # Will see if it can check
                if dealer.canCheck and dealer.getScore(self.cards) > 5000 + random.randint(100, 1000):
                    return self.check()

                # Will bluff
                if self.bluff(dealer.currentBet) and dealer.currentBet != 0:

                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Bluffing but Calling"
                
                # Will Bluff Bet
                elif self.bluff(dealer.currentBet) and dealer.currentBet == 0:
                        
                        betAmount = random.randint(10, random.randint(100, 400))
    
                        if self.bet(betAmount):
    
                            dealer.pot += betAmount
                            dealer.currentBet = betAmount
                            dealer.changeCheck()
                            self.matchedBet = dealer.currentBet
    
                            return "Bluffing but Betted " + str(betAmount)

                # Will have to change the numer thing, will bet
                if dealer.getScore(self.cards) < 6000:
                    
                    # If doing really well, it will bet
                    if dealer.getScore(self.cards) < 3000:
                            
                            betAmount = random.randint(0, self.money)
                            if self.bet(betAmount):
        
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                dealer.changeCheck()
                                self.matchedBet = dealer.currentBet
        
                                return "Betted " + str(betAmount)
                            
                    betAmount = random.randint(10, (200 * self.difficulty + 50))

                    if self.bet(betAmount):

                        dealer.pot += betAmount
                        dealer.currentBet = betAmount
                        dealer.changeCheck()
                        self.matchedBet = dealer.currentBet

                        return "Betted " + str(betAmount)

                # Last resort
                if dealer.canCheck:
                    return self.check() + " Last Resort"
                
                # Will match minor Bets, bc why not
                if dealer.currentBet == 10 or dealer.currentBet == 20 or dealer.currentBet == 30 or dealer.currentBet == 40 or dealer.currentBet == 50:
                    
                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
                
                # Will match bigger bets based on difficulty
                if dealer.currentBet >= 100 and random.randint(0, 100) < self.difficulty * 20 + 10:

                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
                

                # This will fold
                self.folded = True
                return "Folding"
            
            # If it cant bet
            else:

                # Will match the bet 
                if dealer.currentBet != self.matchedBet:

                    # If it can match the current bet
                    if self.call(dealer.currentBet - self.matchedBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Matching Bet"
                    
                    # Will raise the bet if feeling it
                    if (dealer.getScore(self.cards) < 4000 + random.randint(100, 400) - (400 * self.difficulty)) and self.money >= dealer.currentBet:
                            
                            betAmount = random.randint(10, (200 * self.difficulty + 50))
    
                            if self.bet(betAmount):
    
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                self.matchedBet = dealer.currentBet
                                return "Raising Bet " + str(betAmount)
                    
                    # Will go all in if it does not have enough money
                    if (dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (400 * self.difficulty)) and self.money <= (dealer.currentBet - self.matchedBet):

                        self.allIn()
                        self.money = 0
                        return "All In"
                    
                    else:
                        self.folded = True
                        return "Folding"
                
                elif dealer.currentBet == self.matchedBet:

                    return "Already Matched Bet"
                
                # If it can call, it will probably
                if (dealer.getScore(self.cards) < 5000 + random.randint(100, 1500) - (400 * self.difficulty)) and self.money >= dealer.currentBet:

                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
        
                # Will go all in
                if dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (400 * self.difficulty) and self.money <= dealer.currentBet:

                    self.allIn()
                    self.money = 0
                    return "All In"
                
                 # Will fold
                
                else:
                    
                    self.folded = True
                    return "Folding"

        # Higher difficulty
        elif self.difficulty >= 3 and self.difficulty <= 3.9:
                 # If the bot can bet or check or fold
            if dealer.currentBet == 0:

                # Will see if it can check
                if dealer.canCheck and dealer.getScore(self.cards) > 5000 + random.randint(100, 700):
                    return self.check()

                # Will bluff
                if self.bluff(dealer.currentBet) and dealer.currentBet != 0:

                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Bluffing but Calling"
                
                # Will Bluff Bet
                elif self.bluff(dealer.currentBet) and dealer.currentBet == 0:
                        
                        betAmount = random.randint(10, random.randint(100, 550))
    
                        if self.bet(betAmount):
    
                            dealer.pot += betAmount
                            dealer.currentBet = betAmount
                            dealer.changeCheck()
                            self.matchedBet = dealer.currentBet
    
                            return "Bluffing but Betted " + str(betAmount)

                # Will have to change the numer thing, will bet
                if dealer.getScore(self.cards) < 6000:
                    
                    # If doing really well, it will bet
                    if dealer.getScore(self.cards) < 3000:
                            
                            betAmount = random.randint(0, self.money)
                            if self.bet(betAmount):
        
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                dealer.changeCheck()
                                self.matchedBet = dealer.currentBet
        
                                return "Betted " + str(betAmount)
                            
                    betAmount = random.randint(10, (250 * self.difficulty + 50))

                    if self.bet(betAmount):

                        dealer.pot += betAmount
                        dealer.currentBet = betAmount
                        dealer.changeCheck()
                        self.matchedBet = dealer.currentBet

                        return "Betted " + str(betAmount)

                # Last resort
                if dealer.canCheck:
                    return self.check() + " Last Resort"
                
                # Will match minor Bets, bc why not
                if dealer.currentBet == 10 or dealer.currentBet == 20 or dealer.currentBet == 30 or dealer.currentBet == 40 or dealer.currentBet == 50:
                    
                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
                
                # Will match bigger bets based on difficulty
                if dealer.currentBet >= 100 and random.randint(0, 100) < self.difficulty * 2.5 + 10:

                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
                

                # This will fold
                self.folded = True
                return "Folding"
            
            # If it cant bet
            else:

                # Will match the bet 
                if dealer.currentBet != self.matchedBet:

                    # If it can match the current bet
                    if self.call(dealer.currentBet - self.matchedBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Matching Bet"
                    
                    # Will raise the bet if feeling it
                    if (dealer.getScore(self.cards) < 4000 + random.randint(100, 400) - (300 * self.difficulty)) and self.money >= dealer.currentBet:
                            
                            betAmount = random.randint(10, (200 * self.difficulty + 50))
    
                            if self.bet(betAmount):
    
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                self.matchedBet = dealer.currentBet
                                return "Raising Bet " + str(betAmount)
                    
                    # Will go all in if it does not have enough money
                    if (dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (300 * self.difficulty)) and self.money <= (dealer.currentBet - self.matchedBet):

                        self.allIn()
                        self.money = 0
                        return "All In"
                    
                    else:
                        self.folded = True
                        return "Folding"
                
                elif dealer.currentBet == self.matchedBet:

                    return "Already Matched Bet"
                
                # If it can call, it will probably
                if (dealer.getScore(self.cards) < 5000 + random.randint(100, 1500) - (300 * self.difficulty)) and self.money >= dealer.currentBet:

                    # Will match the bet
                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Calling"
        
                # Will go all in
                if dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (300 * self.difficulty) and self.money <= dealer.currentBet:

                    self.allIn()
                    self.money = 0
                    return "All In"
                
                 # Will fold
                
                else:
                    
                    self.folded = True
                    return "Folding"

        # This is the Impossible difficuluty, it knows what you have, but will still loose, but very rarely
        elif self.difficulty >= 4 and self.difficulty <= 4.9:

            # Anything here will see the cards it has, and will move acordingly
            if dealer.currentBet == 0:

                # Will see if it can check, it will check if it knows you have better cards than it
                if dealer.canCheck and ((dealer.getScore(self.cards) > dealer.getScore(player.cards) - random.randint(100, 250 * self.difficulty)) or (dealer.getScore(self.cards) > dealer.getScore(bot.cards) + random.randint(100, 250 * self.difficulty))):
                    return self.check()

                # Will bluff
                if self.bluff(dealer.currentBet) and dealer.currentBet != 0 and ((dealer.getScore(self.cards) > dealer.getScore(player.cards) - random.randint(100, 200 * self.difficulty)) or (dealer.getScore(self.cards) > dealer.getScore(bot.cards) - random.randint(100, 200 * self.difficulty))):

                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Bluffing but Calling"
                
                # Will Bluff Bet
                elif self.bluff(dealer.currentBet) and dealer.currentBet == 0 and ((dealer.getScore(self.cards) > dealer.getScore(player.cards) - random.randint(100, 200 * self.difficulty)) or (dealer.getScore(self.cards) > dealer.getScore(bot.cards) - random.randint(100, 200 * self.difficulty))):
                        
                        betAmount = random.randint(10, random.randint(100, 200))
    
                        if self.bet(betAmount):
    
                            dealer.pot += betAmount
                            dealer.currentBet = betAmount
                            dealer.changeCheck()
                            self.matchedBet = dealer.currentBet
    
                            return "Bluffing but Betted " + str(betAmount)

                # Will bet
                if ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))) or random.randint(0, 100) < 10 * self.difficulty:
                    
                    # If doing really well, it will bet
                    if ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):
                            
                            betAmount = random.randint(0, self.money)
                            if self.bet(betAmount):
        
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                dealer.changeCheck()
                                self.matchedBet = dealer.currentBet
        
                                return "Betted " + str(betAmount)
                            
                    betAmount = random.randint(10, (150 * self.difficulty + 50))

                    if self.bet(betAmount):

                        dealer.pot += betAmount
                        dealer.currentBet = betAmount
                        dealer.changeCheck()
                        self.matchedBet = dealer.currentBet

                        return "Betted " + str(betAmount)

                # Last resort
                if dealer.canCheck:
                    return self.check() + " Last Resort"
                
            
                # Will match the bet 
            
            # If it cant check
            elif dealer.currentBet != self.matchedBet:
                    
                    # Will raise the bet if feeling it
                    if self.money >= dealer.currentBet and ((dealer.getScore(self.cards) < dealer.getScore(player.cards) - random.randint(50, 100 * self.difficulty)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards) - random.randint(50, 100 * self.difficulty))):
                            
                            betAmount = random.randint(10, (150 * self.difficulty + 50))
    
                            if self.bet(betAmount):
    
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                self.matchedBet = dealer.currentBet
                                return "Raising Bet " + str(betAmount)

                    # If it can match the current bet
                    if  self.money < (dealer.currentBet - self.matchedBet) and ((dealer.getScore(self.cards) < dealer.getScore(player.cards) - random.randint(50, 200 * self.difficulty)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards) - random.randint(50, 200 * self.difficulty))):
                        
                        self.call(dealer.currentBet - self.matchedBet)
                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Matching Bet"
                              
                    # Will go all in if it does not have enough money
                    if (dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (300 * self.difficulty)) and self.money <= (dealer.currentBet - self.matchedBet) and ((dealer.getScore(self.cards) < dealer.getScore(player.cards) - random.randint(10, 50 * self.difficulty)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards) - random.randint(10, 50 * self.difficulty))):

                        self.allIns()
                        self.money = 0
                        return "All In"
                    
                    else:
                        self.folded = True
                        return "Folding"
                
            elif dealer.currentBet == self.matchedBet:
                return "Already Matched Bet"
            
            # If it can call, it will probably
            if (dealer.getScore(self.cards) < 5000 + random.randint(100, 1500) - (300 * self.difficulty)) and self.money >= dealer.currentBet and ((dealer.getScore(self.cards) < dealer.getScore(player.cards) - random.randint(50, 200 * self.difficulty)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards) - random.randint(50, 200 * self.difficulty))):

                # Will match the bet
                if self.call(dealer.currentBet):

                    dealer.pot += dealer.currentBet
                    self.matchedBet = dealer.currentBet
                    return "Calling"
    
            # Will go all in
            if dealer.getScore(self.cards) < 3000 + random.randint(100, 200) - (300 * self.difficulty) and self.money <= dealer.currentBet and ((dealer.getScore(self.cards) < dealer.getScore(player.cards) - random.randint(10, 50 * self.difficulty)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards) - random.randint(10, 50 * self.difficulty))):

                self.allIn()
                self.money = 0
                return "All In"
            
                # Will fold

            # This probably does not get used
            if dealer.currentBet <= 50 * self.difficulty:
                
                # Will match the bet
                if self.call(dealer.currentBet):

                    dealer.pot += dealer.currentBet
                    self.matchedBet = dealer.currentBet
                    return "Calling"
            
            # Will match bigger bets based on difficulty
            if dealer.currentBet >= 50 * self.difficulty and ((dealer.getScore(self.cards) < dealer.getScore(player.cards) - random.randint(50, 150 * self.difficulty)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards) - random.randint(50, 150 * self.difficulty))):

                # Will match the bet
                if self.call(dealer.currentBet):

                    dealer.pot += dealer.currentBet
                    self.matchedBet = dealer.currentBet
                    return "Calling"
                     
            else:
                
                self.folded = True
                return "Folding"
                
        # Cheater Difficulty, it will not loose unless you have higher cards than it, thats it :)
        else:

             # Anything here will see the cards it has, and will move acordingly
            if dealer.currentBet == 0:

                # Will see if it can check, it will check if it knows you have better cards than it
                if dealer.canCheck and ((dealer.getScore(self.cards) > dealer.getScore(player.cards)) or (dealer.getScore(self.cards) > dealer.getScore(bot.cards))):
                    return self.check()

                # Will bluff
                if self.bluff(dealer.currentBet) and dealer.currentBet != 0 and ((dealer.getScore(self.cards) > dealer.getScore(player.cards)) or (dealer.getScore(self.cards) > dealer.getScore(bot.cards))):

                    if self.call(dealer.currentBet):

                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Bluffing but Calling"
                
                # Will Bluff Bet
                elif self.bluff(dealer.currentBet) and dealer.currentBet == 0 and ((dealer.getScore(self.cards) > dealer.getScore(player.cards)) or (dealer.getScore(self.cards) > dealer.getScore(bot.cards))):
                        
                        betAmount = random.randint(10, random.randint(100, 200))
    
                        if self.bet(betAmount):
    
                            dealer.pot += betAmount
                            dealer.currentBet = betAmount
                            dealer.changeCheck()
                            self.matchedBet = dealer.currentBet
    
                            return "Bluffing but Betted " + str(betAmount)

                # Will bet
                if ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):
                    
                    # If doing really well, it will bet
                    if ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):
                            
                            betAmount = random.randint(0, self.money)
                            if self.bet(betAmount):
        
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                dealer.changeCheck()
                                self.matchedBet = dealer.currentBet
        
                                return "Betted " + str(betAmount)
                            
                    betAmount = random.randint(10, (150 * self.difficulty + 50))

                    if self.bet(betAmount):

                        dealer.pot += betAmount
                        dealer.currentBet = betAmount
                        dealer.changeCheck()
                        self.matchedBet = dealer.currentBet

                        return "Betted " + str(betAmount)

                # Last resort
                if dealer.canCheck:
                    return self.check() + " Last Resort"
                
            # If it cant check
            elif dealer.currentBet != self.matchedBet:
                    
                    # Will raise the bet if feeling it
                    if self.money >= dealer.currentBet and ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):
                            
                            betAmount = random.randint(10, (150 * self.difficulty + 50))
    
                            if self.bet(betAmount):
    
                                dealer.pot += betAmount
                                dealer.currentBet = betAmount
                                self.matchedBet = dealer.currentBet
                                return "Raising Bet " + str(betAmount)

                    # If it can match the current bet
                    if  self.money < (dealer.currentBet - self.matchedBet) and ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):
                        
                        self.call(dealer.currentBet - self.matchedBet)
                        dealer.pot += dealer.currentBet
                        self.matchedBet = dealer.currentBet
                        return "Matching Bet"
                              
                    # Will go all in if it does not have enough money
                    if self.money <= (dealer.currentBet - self.matchedBet) and ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):

                        self.allIns()
                        self.money = 0
                        return "All In"
                    
                    else:
                        self.folded = True
                        return "Folding"
                
            elif dealer.currentBet == self.matchedBet:
                return "Already Matched Bet"
            
            # If it can call, it will probably
            if  self.money >= dealer.currentBet and ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):

                # Will match the bet
                if self.call(dealer.currentBet):

                    dealer.pot += dealer.currentBet
                    self.matchedBet = dealer.currentBet
                    return "Calling"
    
            # Will go all in
            if self.money <= dealer.currentBet and ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):

                self.allIns()
                self.money = 0
                return "All In"

            # This probably does not get used
            if dealer.currentBet <= 50 * self.difficulty:
                
                # Will match the bet
                if self.call(dealer.currentBet):

                    dealer.pot += dealer.currentBet
                    self.matchedBet = dealer.currentBet
                    return "Calling"
            
            # Will match bigger bets based on difficulty
            if dealer.currentBet >= 50 * self.difficulty and ((dealer.getScore(self.cards) < dealer.getScore(player.cards)) or (dealer.getScore(self.cards) < dealer.getScore(bot.cards))):

                # Will match the bet
                if self.call(dealer.currentBet):

                    dealer.pot += dealer.currentBet
                    self.matchedBet = dealer.currentBet
                    return "Calling"
                     
            else:

                self.folded = True
                return "Folding"


            
            
