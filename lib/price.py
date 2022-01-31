import abc
from lib import fndate

class Component(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def format(self):
		pass

	@abc.abstractmethod
	def get_children(self):
		pass

	@abc.abstractmethod
	def is_leaf(self):
		pass

	def price(self):
		return self._price

	def start(self):
		return self._start

	def description(self):
		return self._descr

	def type(self):
		return self._type

	def end(self):
		return self._end

	def deep(self):
		return self._deep

	def set_deep(self, deep):
		if self.is_leaf():
			self._deep = deep
		else:
			self._deep = deep
			for child in self._children:
				child.set_deep(deep + 1)

class Prices(Component):
	def __init__(self):
		self._children = []
		self._price = 0
		self._start = None
		self._end = None
		self._deep = 0
		self._type = None

	def append(self, component):
		if component.start() != None and component.end() != None:
			component.set_deep(self._deep + 1)
			self._children.append(component)
			self._price += component.price()
			if self._start == None or self._start > component.start():
				self._start =  component.start()
			if self._end == None or self._end < component.end():
				self._end =  component.end()
			self._diff = (self._end - self._start).days + 1

			self._children.sort(key=lambda x: x.start())

	def format(self, verbose=False):
		if self._price != 0 or verbose:
			text = "%s+ %s -> %s (%d)\t [%.2f]\n" % ('   '*self._deep, fndate.format(self._start), fndate.format(self._end), self._diff, self._price)
			for child in self._children:
				text += child.format(verbose)
		else:
			text = ''
		return text

	def get_children(self):
		return self._children

	def is_leaf(self):
		return False

	def __len__(self):
		return len(self._children)

	def last(self):
		if len(self._children) > 0:
			return self._children[-1]
		return None

class Price(Component):
	def __init__(self, start, end, price, descr, type):
		self._start = start
		self._end = end
		self._diff = (end - start).days + 1
		self._price = price
		self._descr = descr
		self._deep = 0
		self._type = type

	def format(self, verbose=False):
		if self._price != 0 or verbose:
			if self._end == self._start:
				return "%s| %s \t (%d)\t [%.2f] %s\n" % ('   '*(self._deep), fndate.format(self._start), self._diff, self._price, self._descr)
			else:
				return "%s| %s -> %s (%d)\t [%.2f] %s\n" % ('   '*(self._deep), fndate.format(self._start), fndate.format(self._end), self._diff, self._price, self._descr)
		return ''

	def get_children(self):
		return None

	def is_leaf(self):
		return True

	def description(self):
		return self._descr

# ~@:-]