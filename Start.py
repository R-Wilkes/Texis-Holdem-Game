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
currentBet = 0

# Initialize dealer and players
dealer = Dealer.Dealer("Dealer", deck, [])
player = Person.Person("Ricker", startingMoney, dealer.dealCards())
bot1 = Bot.Bot("AI1", startingMoney, dealer.dealCards())
bot2 = Bot.Bot("AI2", startingMoney, dealer.dealCards())

# Starts the game
dealer.startGame()

# Main Game Loop
while True:

    print("\n" * 5)
    print("Current Bet: " + str(currentBet))
    print("Dealer:", dealer.board)
    print(player.name + ": " + str(player.getCards()))
    print(bot1.name + ": " + "** **")
    print(bot2.name + ": " + "** **")


    # If player turn
    if player.isTurn and player.folded == False:

        # Player's turn
        action = input("Check, Bet, or Fold? ")

        # For checking
        if action.lower() == "check" and currentBet == 0:

            print("Checking")
            dealer.nextTurn(player, bot1, bot2)
        
        # For betting
        elif action.lower() == "bet":

            print("Betting")

            # Checks there bet to see if its valid
            if player.bet(int(input("How much would you like to bet? "))) == False:
                print("Not enough money")

            else:
                dealer.nextTurn(player, bot1, bot2)

        # For folding
        elif action.lower() == "fold":

            print("Folding")
            player.fold()

            dealer.nextTurn(player, bot1, bot2)

        else:
            print("Not an Option")

    # For bot1 turn
    if bot1.isTurn:

        print("AI1's Turn")
        dealer.nextTurn(player, bot1, bot2)
        sleep(2)

    # For bot2 turn
    if bot2.isTurn:

        print("AI2's Turn")
        dealer.nextTurn(player, bot1, bot2)
        sleep(2)
    
   









# # Deal some cards
# board = [deck.draw(1)[0] for _ in range(5)]  # Correctly extract each card from the list
# hand = [deck.draw(1)[0] for _ in range(2)]   # Correctly extract each card from the list

# # Print cards in a readable format
# print("Board:", [Card.int_to_pretty_str(card) for card in board])
# print("Hand:", [Card.int_to_pretty_str(card) for card in hand])

# # Evaluate the hand
# score = evaluator.evaluate(hand, board)
# hand_class = evaluator.get_rank_class(score)

# print("Hand class:", evaluator.class_to_string(hand_class))
