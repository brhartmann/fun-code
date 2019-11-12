from Card import *

class Row:
	Color = Colors.YELLOW
	#Discards = []

	def __init__(self, color):
		self.Color = color
		self.Discards = []

class GameBoard:
	Rows = []

	def __init__(self, playerOne, playerTwo, deck):
		self.PlayerOne = playerOne
		self.PlayerTwo = playerTwo
		self.Deck = deck
		for color in Colors:
			self.Rows.append(Row(color))

	def Discard(self, card):
		matchingRow = next(r for r in self.Rows if r.Color == card.Color)
		matchingRow.Discards.append(card)
		
	def TotalDiscards(self):
		total = 0
		for row in self.Rows:
			total += len(row.Discards)
		return total

	def DisplayBoard(self):
		print("")
		self.PlayerOne.PrintPlayerInfo()
		self.PlayerTwo.PrintPlayerInfo()
		print("")
		for row in self.Rows:
			disc = "  "
			plrOnePlayed = ""
			plrTwoPlayed = ""

			if len(row.Discards) > 0:
				disc = row.Discards[-1].ShortDisplay()

			matchingExpedition = next(e for e in self.PlayerOne.Expeditions if e.Color == row.Color)
			plrOnePlayed = matchingExpedition.DisplayCards(True)
			while len(plrOnePlayed) < 25:
				plrOnePlayed = " " + plrOnePlayed

			matchingExpedition = next(e for e in self.PlayerTwo.Expeditions if e.Color == row.Color)
			plrTwoPlayed = matchingExpedition.DisplayCards(False)

			print("%s | %s | %s" % (plrOnePlayed, disc, plrTwoPlayed))

		print("")
		print(" " * 11 + "Cards Remaining: %d" % len(self.Deck.Cards))
