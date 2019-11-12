from Player import *

class BasicAIPlayer(Player):
	def __init__(self, name, startingCards):
		self.ShortType = "B"
		Player.__init__(self, name, startingCards)

	def PlayCard(self, gameBoard, remainingDeckCount, opponentExpeditions):	
		illegalCards = []
		while len(illegalCards) < len(self.Hand):
			lowCard = self.FindLowestValueCardInHand(illegalCards)
			matchingExpedition = self.MatchingExpedition(lowCard.Color, self.Expeditions)
			if matchingExpedition.CanPlayCard(lowCard):
				self.Hand.remove(lowCard)
				matchingExpedition.PlayCard(lowCard)
				break
			illegalCards.append(lowCard)
		else:  # no legal plays, need to discard
			dummyList = []
			lowCard = self.FindLowestValueCardInHand(dummyList)
			matchingExpedition = self.MatchingExpedition(lowCard.Color, self.Expeditions)
			self.Hand.remove(lowCard)
			gameBoard.Discard(lowCard)

	def DrawCard(self, deck, gameBoard, opponentExpeditions):
		drawCard = deck.DrawCard()
		self.Hand.append(drawCard)
		Player.DrawCard(self, None, None, None)

	def FindLowestValueCardInHand(self, skipCards):
		lowCard = None
		for card in self.Hand:
			if card in skipCards:
				continue
			if (lowCard == None or card.Value < lowCard.Value):
				lowCard = card
		return lowCard
