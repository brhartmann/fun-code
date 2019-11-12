from Player import *
from BasicAIPlayer import BasicAIPlayer

class AdvancedAIPlayer(BasicAIPlayer):
	def __init__(self, name, startingCards):
		self.ShortType = "A"
		Player.__init__(self, name, startingCards)

	def PlayCard(self, gameBoard, remainingDeckCount, opponentExpeditions):
		# Rank effectiveness (value added) of each potential play:
		bestCardToPlay = None
		shouldDiscard = False
		bestValueAdded = -99
		for card in self.Hand:
			oppCanUse = self._OpponentCanUse(card, opponentExpeditions)
			dropValue = 10
			if oppCanUse:
				dropValue = -2 * ((card.Investment * 7) + card.Value)

			if dropValue > bestValueAdded:
				bestValueAdded = dropValue
				bestCardToPlay = card
				shouldDiscard = True

			matchingExpedition = self.MatchingExpedition(card.Color, self.Expeditions)
			urgency = self._Urgency(remainingDeckCount)
			committed = self._Committed(matchingExpedition)
			if not committed and urgency > 6:  
				continue  # avoid starting a new expedition too late in the game

			opponentExpedition = self.MatchingExpedition(card.Color, opponentExpeditions)
			potential = self._GetPotentialTotal(card, opponentExpedition)
			netPotential = potential - matchingExpedition.Score()
			cardgap = self._CardGap(card, matchingExpedition, opponentExpedition)

			riskAdjustment = 0
			if not committed:
				riskAdjustment = int((urgency * matchingExpedition.Score([card])) / 10)

			# TODO : improve this formula with AI training
			valueAdded = int(netPotential * 3 / (cardgap + 1)) + riskAdjustment

			if valueAdded > bestValueAdded:
				bestValueAdded = valueAdded
				bestCardToPlay = card
				shouldDiscard = False		

			#print("%s: potential=%d, valueAdded=%d, dv=%d" % (card.ShortDisplay(), potential, valueAdded, dropValue))

		self.Hand.remove(bestCardToPlay)
		if shouldDiscard:
			gameBoard.Discard(bestCardToPlay)
		else:
			self.MatchingExpedition(bestCardToPlay.Color, self.Expeditions).PlayCard(bestCardToPlay)

	def DrawCard(self, deck, gameBoard, opponentExpeditions):
		interestingDiscard = None
		interestingRow = None
		safetyDiscard = None  # for the "must draw a discard to delay game clock" scenario
		safetyRow = None
		discRank = -5
		for row in gameBoard.Rows:
			if len(row.Discards) > 0:
				disc = row.Discards[-1]
				safetyDiscard = disc
				safetyRow = row 
				matchingExpedition = self.MatchingExpedition(row.Color, self.Expeditions)
				opponentExpedition = self.MatchingExpedition(row.Color, opponentExpeditions)
				if (matchingExpedition.CanPlayCard(disc) == True and self._ShouldPlayCard(disc, len(deck.Cards), opponentExpedition)):
					tempRank = disc.Value + (2 * (self._CardGap(disc, matchingExpedition, opponentExpedition)))
					if (tempRank > discRank):
						discRank = tempRank
						tempRow = row
						interestingDiscard = disc

		# TODO : enhance AI with eval of whether a discard of great value to opponent should be picked up		
		drawCard = interestingDiscard
		if drawCard == None:
			if safetyDiscard != None and self._MustDrawFromDiscards(len(deck.Cards), gameBoard.TotalDiscards()):
				drawCard = safetyDiscard
				safetyRow.Discards.remove(drawCard)
			else:
				drawCard = deck.DrawCard()
		else:
			tempRow.Discards.remove(interestingDiscard)
		self.Hand.append(drawCard)
		Player.DrawCard(self, None, None, None)

	def _ShouldPlayCard(self, card, remainingDeckCount, opponentExpedition):
		discardValue = 0
		if (card not in self.Hand): # evaluate a potential pickup from the discard pile
			discardValue = card.Value

		potential = self._GetPotentialTotal(card, opponentExpedition) + discardValue

		return potential > 10

	def _GetPotentialTotal(self, potCard, opponentExpedition):
		matchingExpedition = self.MatchingExpedition(potCard.Color, self.Expeditions)
		if not matchingExpedition.CanPlayCard(potCard):
			return -99

		total = 0
		investment = 1
		cardCount = 0
		unseenValues = Card.GetValuesList()

		matchingCards = list(filter(lambda x: x.Color == potCard.Color, self.Hand))
		for card in matchingCards:
			unseenValues.remove(card.Value)
			if card.Value >= potCard.Value:
				total += card.Value
				cardCount += 1
				investment += card.Investment
		try:
			for card in matchingExpedition.Cards:
				unseenValues.remove(card.Value)
				total += card.Value
				cardCount += 1
				investment += card.Investment
		except ValueError:
			print("cardVal: %d" % card.Value)
			print(*unseenValues)
			for card in matchingCards:
				print(card.ShortDisplay())

		for card in opponentExpedition.Cards:
			if card.Value > 0:
				unseenValues.remove(card.Value)

		# account for cards which might be drawn, assuming 50% probability
		# for now don't count unseen investment cards - these are unlikely to be drawn in time to use
		unseenPotential = 0
		unseenCardCount = 0
		for val in unseenValues:
			if val > potCard.Value:
				unseenPotential += val
				unseenCardCount += 1
		total += int(0.5 * unseenPotential)
		cardCount += int(0.5 * unseenCardCount)

		return Expedition.CalculateScore(total, investment, cardCount)

	# Factors for decision-making:

	def _Urgency(self, remainingDeckCount):
		urgencyFactors = [1, 1, 2, 2, 3, 4, 6, 8, 12, 99]
		index = int((45 - remainingDeckCount) / 5 )
		return urgencyFactors[index]

	def _Committed(self, expedition):
		return len(expedition.Cards) > 0

	def _CardGap(self, card, expedition, opponentExpedition):
		gap = card.Value - expedition.LargestPlayedValue()

		if gap <= 0:
			return 1

		for n in range(expedition.LargestPlayedValue(), card.Value):
			for oppCard in opponentExpedition.Cards:
				if oppCard.Value == n:
					gap -= 1
					break

		if expedition.LargestPlayedValue() == 0 and card.Value > 0:
			investmentsPlayed = sum(1 for c in expedition.Cards if c.Investment == 1)
			gap += ((3 - investmentsPlayed) - 1)

		return gap

	def _OpponentCanUse(self, card, opponentExpeditions):
		return self.MatchingExpedition(card.Color, opponentExpeditions).CanPlayCard(card)

	def _MustDrawFromDiscards(self, remainingDeckCount, discardsCount):
		if discardsCount == 0:
			return False
		
		playableCardsInHand = 0
		for card in self.Hand:
			if self.MatchingExpedition(card.Color, self.Expeditions).CanPlayCard(card):
				playableCardsInHand += 1

		return playableCardsInHand >= remainingDeckCount