from enum import Enum
from Card import *
from Expedition import Expedition

class PlayerType(Enum):
	Human = 1,
	BasicAI = 2,
	AdvancedAI = 3

class Player:
	Name = ""
	ShortType = "H" # for display only
	#Hand = [] # list of Cards
	#Expeditions = []

	def __init__(self, name, startingCards):
		self.Name = name
		self.Hand = []
		self.Expeditions = []
		for card in startingCards:
			self.Hand.append(card)
		list.sort(self.Hand, key=lambda card: card.SortValue)
		for color in Colors:
			self.Expeditions.append(Expedition(color))

	def Score(self):
		total = 0
		for exp in self.Expeditions:
			total += exp.Score()
		return total

	# if card is played on a discard pile, return the card, else return None
	def PlayCard(self, gameBoard, remainingDeckCount, opponentExpeditions):
		pass

	def DrawCard(self, deck, gameBoard, opponentExpeditions):
		list.sort(self.Hand, key=lambda card: card.SortValue)

	def DisplayHand(self):
		display = ""
		for card in self.Hand:
			display += card.ShortDisplay()
			display += " "
		return display

	def PrintPlayerInfo(self):
		print("%s (%s) -- Score: %d, Hand: %s" % (self.Name, self.ShortType, self.Score(), self.DisplayHand()))

	# tried making this static but that led to problems
	def MatchingExpedition(self, color, expeditions):
		return next(e for e in expeditions if e.Color == color)