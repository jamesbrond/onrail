"""Prices"""
import abc
from lib import fndate


class Component(metaclass=abc.ABCMeta):
    """Component abstract class"""

    def __init__(self):
        self._children = []
        self._price = 0
        self._start = None
        self._end = None
        self._deep = 0
        self._type = None
        self._diff = 0
        self._descr = ''

    @abc.abstractmethod
    def format(self):
        """Format"""

    @abc.abstractmethod
    def get_children(self):
        """get child nodes"""

    @abc.abstractmethod
    def is_leaf(self):
        """is a leaf node"""

    def price(self):
        """total price"""
        return self._price

    def start(self):
        """start date"""
        return self._start

    def description(self):
        """description"""
        return self._descr

    def type(self):
        """type"""
        return self._type

    def end(self):
        """end date"""
        return self._end

    def deep(self):
        """Deep"""
        return self._deep

    def set_deep(self, deep):
        """set deep"""
        if self.is_leaf():
            self._deep = deep
        else:
            self._deep = deep
            for child in self._children:
                child.set_deep(deep + 1)

class Prices(Component):
    """Composition of Price classes"""

    def append(self, component):
        """Append"""
        if component.start() is not None and component.end() is not None:
            component.set_deep(self._deep + 1)
            self._children.append(component)
            self._price += component.price()
            if self._start is None or self._start > component.start():
                self._start =  component.start()
            if self._end is None or self._end < component.end():
                self._end =  component.end()
            self._diff = (self._end - self._start).days + 1

            self._children.sort(key=lambda x: x.start())

    def format(self, verbose=False):
        if self._price != 0 or verbose:
            text = "%s+ %s -> %s (%d)\t [%.2f]\n" % ('   '*self._deep, fndate.date_format(self._start), fndate.date_format(self._end), self._diff, self._price)
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
        """last"""
        if len(self._children) > 0:
            return self._children[-1]
        return None

class Price(Component):
    """Price class"""

    def __init__(self, start, end, price, descr, type):
        super().__init__()
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
                return "%s| %s \t (%d)\t [%.2f] %s\n" % ('   '*(self._deep), fndate.date_format(self._start), self._diff, self._price, self._descr)
            else:
                return "%s| %s -> %s (%d)\t [%.2f] %s\n" % ('   '*(self._deep), fndate.date_format(self._start), fndate.date_format(self._end), self._diff, self._price, self._descr)
        return ''

    def get_children(self):
        return None

    def is_leaf(self):
        return True

    def description(self):
        return self._descr

# ~@:-]
