import os
import json
import logging
import webbrowser
from lib import fndate

class CalendarExport:
	def __init__(self, prices):
		self.prices = prices
		self.d = {
			"start": fndate.format(prices.start()),
			"end": fndate.format(prices.end())
		}

	def leaves(self, prices):
		leaves = []
		for child in prices.get_children():
			if child.is_leaf():
				leaves.append(child)
			else:
				leaves.extend(self.leaves(child))
		return leaves

	def to_json(self):
		leaves = self.leaves(self.prices)
		self.d["days"] = []
		for leaf in leaves:
			self.d["days"].append({
				"start": fndate.format(leaf.start()),
				"end": fndate.format(leaf.end()),
				"price": leaf.price(),
				"descr": leaf.description(),
				"type": leaf.type()
			})
		with open('dist/data.js', 'w', encoding='utf-8') as f:
			logging.debug(f"write to 'dist/data.js'")
			f.write("const data = ")
			json.dump(self.d, f)
			webbrowser.open(f"file://{os.path.realpath('dist/index.html')}", new=2)

# ~@:-]