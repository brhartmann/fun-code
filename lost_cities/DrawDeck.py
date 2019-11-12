import random
from Card import *

class DrawDeck:
	Cards = []

	def __init__(self):
		cardNumbers = Card.GetValuesList()
		for color in Colors:
			for val in cardNumbers:
				self.Cards.append(Card(val, color))
		random.shuffle(self.Cards)

	def DrawCard(self):
		#if len(self.Cards) == 0:
		#	return None
		return self.Cards.pop(0)

	def DrawCards(self, quantity = 1):
		drawnCards = []
		for x in range(0, quantity):
			drawnCards.append(self.DrawCard())
		return drawnCards