from Player import *

class HumanPlayer(Player):
	def PlayCard(self, gameBoard, remainingDeckCount, opponentExpeditions):	
		pass	
		# TODO : UI

	def DrawCard(self, deck, gameBoard, opponentExpeditions):
		drawCard = deck.DrawCard()
		self.Hand.append(drawCard)
		Player.DrawCard(self, None, None, None)
		# TODO : UI for choosing between draw deck and discards