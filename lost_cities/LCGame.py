from DrawDeck import DrawDeck
from Player import *
from HumanPlayer import HumanPlayer
from BasicAIPlayer import BasicAIPlayer
from AdvancedAIPlayer import AdvancedAIPlayer
from GameBoard import GameBoard
import time

deck = DrawDeck()

# testing of deck creation:
#for card in deck.Cards:
#	print("Color: %s, Value: %d, Investment: %d" % (card.Color.name, card.Value, card.Investment))

playerOne = BasicAIPlayer("David", deck.DrawCards(8))
playerTwo = AdvancedAIPlayer("Jeff", deck.DrawCards(8))

plrOneActive = True

# testing player creation:
#playerOne.PrintPlayerInfo()
#playerTwo.PrintPlayerInfo()

board = GameBoard(playerOne, playerTwo, deck)
board.DisplayBoard()

# the game ends when draw deck is empty
while len(deck.Cards) > 0:
	# each turn the active player must play a card, then draw a card
	activePlayer = playerOne
	opponent = playerTwo
	if plrOneActive == False:
		activePlayer = playerTwo
		opponent = playerOne

	activePlayer.PlayCard(board, len(deck.Cards), opponent.Expeditions)
	activePlayer.DrawCard(deck, board, opponent.Expeditions)

	#time.sleep(0.5)
	board.DisplayBoard()
	plrOneActive = not plrOneActive
