from enum import Enum

class Colors(Enum):
	YELLOW = 1
	BLUE = 2
	WHITE = 3
	GREEN = 4
	RED = 5

class Card:
	Value = 0
	Color = Colors.YELLOW
	Investment = 0
	SortValue = 0

	def __init__(self, value, color):
		self.Value = value
		self.Color = color
		if value == 0:
			self.Investment = 1
		self.SortValue = ((color.value) * 12) + value

	def ShortDisplay(self):
		display = self._ShortColor(self.Color)
		if self.Investment == 1:
			return display + "$"
		return display + str(self.Value)

	def _ShortColor(self, color):
		letter = {
			Colors.YELLOW: "Y",
			Colors.BLUE: "B",
			Colors.WHITE: "W",
			Colors.GREEN: "G",
			Colors.RED: "R"
		}
		return letter.get(color, "?")

	@classmethod
	def GetValuesList(cls):
		return [0, 0, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
