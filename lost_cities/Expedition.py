from Card import *

class Expedition:
	Color = Colors.YELLOW
	#Cards = []

	def __init__(self, color):
		self.Color = color
		self.Cards = []

	def CanPlayCard(self, card):
		if card.Value < self.LargestPlayedValue():
			return False
		return True

	def LargestPlayedValue(self):
		# assumption: last card in list *should* always be the highest value
		if len(self.Cards) == 0:
			return 0
		return self.Cards[-1].Value

	def PlayCard(self, card):
		self.Cards.append(card)

	def Score(self, potentialCards = []):
		total = 0
		multiplier = 1
		potentialCount = len(self.Cards) + len(potentialCards)

		if potentialCount == 0:  # no commitment yet to this expedition
			return 0

		for card in self.Cards:
			multiplier += card.Investment
			total += card.Value

		for card in potentialCards:
			multiplier += card.Investment
			total += card.Value

		return self.CalculateScore(total, multiplier, potentialCount)

	@staticmethod
	def CalculateScore(total, multiplier, cardCount):
		bonus = 0
		if cardCount >= 8:
			bonus = 20
		return (multiplier * (total - 20)) + bonus

	def DisplayCards(self, reverse):
		playedCardsStr = ""
		
		if reverse == True:
			for card in reversed(self.Cards):
				playedCardsStr += card.ShortDisplay() + " "
		else:
			for card in self.Cards:
				playedCardsStr += card.ShortDisplay() + " "

		return playedCardsStr