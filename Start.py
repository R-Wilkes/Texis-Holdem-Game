from treys import Card, Deck, Evaluator
import Person
import Dealer
import Bot
from time import sleep

# Initialize deck and evaluator
deck = Deck()
evaluator = Evaluator()

# Pre Stuff
startingMoney = 1000

# Initialize dealer and players
dealer = Dealer.Dealer("Dealer", deck)
player = Person.Person("Ricker", startingMoney, dealer.dealCards())

# Difficulty ranges from 1.1 to 3.5
bot1 = Bot.Bot("AI1", startingMoney, dealer.dealCards(), dealer.difficultyDecider())
bot2 = Bot.Bot("AI2", startingMoney, dealer.dealCards(), dealer.difficultyDecider())

# Starts the game
dealer.startGame()

# Main Game Loop
while True:

    print("\n" * 5)
    print("Current Pot: " + str(dealer.pot))
    print("Current Bet: " + str(dealer.currentBet))
    print("Dealer: " + str(dealer.getBoard()) + "\n")
    print(player.name + ": " + str(player.getCards()) + " Money: " + str(player.money) + " Score: " + str(dealer.getScore(player.getCardsInt())) + "\n")

    # If we have cheats on
    if dealer.cheats:

        print(bot1.name + ": " + str(bot1.getCards()) + " Money: " + str(bot1.money) + " Score: " + str(dealer.getScore(bot1.getCardsInt())))
        print(bot2.name + ": " + str(bot2.getCards()) + " Money: " + str(bot2.money) + " Score: " + str(dealer.getScore(bot2.getCardsInt())))
    
    else:

        print(bot1.name + ":  **** Money: " + str(bot1.money) + " Score: ????")
        print(bot2.name + ":  **** Money: " + str(bot2.money) + " Score: ????")
        
    print("\n" * 2)

    # If player turn
    if player.isTurn and player.folded == False:

        # Player's turn
        action = input(player.getOptions(dealer))

        # For checking
        if (action.lower()).strip()  == "check" and dealer.currentBet == 0:

            print("Checking")
            dealer.changeCheck()
            dealer.nextTurn(player, bot1, bot2)
        
        # For betting
        elif (action.lower()).strip()  == "bet":

            print("Betting")
            betAmount = int(input("How much would you like to bet? "))

            # Checks there bet to see if its valid
            if player.bet(betAmount) == False:
                print("Not enough money")

            else:

                dealer.currentBet = betAmount
                dealer.pot += betAmount
                dealer.changeCheck()
                dealer.nextTurn(player, bot1, bot2)

        # For folding
        elif (action.lower()).strip()  == "fold":

            print("Folding")
            player.fold()

            dealer.nextTurn(player, bot1, bot2)

        # For calling
        elif (action.lower()).strip()  == "call":

            dealer.pot += dealer.currentBet
            player.money -= dealer.currentBet - player.matchedBet
            player.matchedBet = dealer.currentBet
            dealer.changeCheck()
            dealer.nextTurn(player, bot1, bot2)
            print("Calling")

        # For raising
        elif (action.lower()).strip() == "raise":

            print("Raising")
            raiseAmount = int(input("How much would you like to raise? "))

            # Checks there bet to see if its valid
            if player.bet(raiseAmount) == False:
                print("Not enough money")

            else:

                dealer.currentBet += raiseAmount
                dealer.pot += raiseAmount
                dealer.changeCheck()
                dealer.nextTurn(player, bot1, bot2)

        else:
            print("Not an Option")

    # For bot1 turn
    if bot1.isTurn and bot1.folded == False:
            

            print(" \nAI1's Turn")
            print(bot1.decideMove(dealer, player, bot2))
            dealer.nextTurn(player, bot1, bot2)
            print("\n")
            sleep(1)

    # For bot2 turn
    if bot2.isTurn and bot2.folded == False:

            print("AI2's Turn")
            print(bot2.decideMove(dealer, player, bot1))
            dealer.nextTurn(player, bot1, bot2)
            print("\n")
            sleep(1)    


    # Will end the game and determine the winner
    if len(dealer.board) == 5 and dealer.betsMatched(player, bot1, bot2):

        winner = dealer.getWinner(player, bot1, bot2)
        print("\n" * 10)
        print("Dealer: " + str(dealer.getBoard()) + "\n")
        print("Winner is " + winner[0].name + " With: " + str(winner[0].getCards()) + " Of: " + str(dealer.cardClass(winner[0].getCardsInt())))
        winner[0].money += dealer.pot
        dealer.resetGame(player, bot1, bot2)
        sleep(10)
    
    # Will end round and draw a new card
    elif dealer.canCheck and dealer.currentBet == 0 and len(dealer.board) < 5:

        print("Drawing new card")
        dealer.drawCard()
        dealer.resetRound(player, bot1, bot2)

    # Will continue till bets are matched
    elif dealer.betsMatched(player, bot1, bot2) and dealer.amountIn(player, bot1, bot2) >= 2:

        print("All Bets Matched")
        dealer.drawCard()
        dealer.resetRound(player, bot1, bot2)
    
    # Will end the game if all players fold
    elif bot1.folded and bot2.folded:

        print("Player Wins round!!")
        player.money += dealer.pot
        dealer.resetGame(player, bot1, bot2)

    sleep(1)
