import date_utils
import abc
from colors import color

class Component(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def format(self):
        pass

    @abc.abstractmethod
    def getChildren(self):
        pass

    @abc.abstractmethod
    def isLeaf(self):
        pass

    def getPrice(self):
        return self._price

    def getStart(self):
        return self._start

    def getEnd(self):
        return self._end

    def setDeep(self, deep):
        if self.isLeaf():
            self._deep = deep
        else:
            self._deep = deep
            for child in self._children:
                child.setDeep(deep + 1)

class Prices(Component):
    def __init__(self):
        self._children = []
        self._price = 0
        self._start = None
        self._end = None
        self._deep = 0

    def append(self, component):
        if component.getStart() != None and component.getEnd() != None:
            component.setDeep(self._deep + 1)
            self._children.append(component)
            self._price += component.getPrice()
            if self._start == None or self._start > component.getStart():
                self._start =  component.getStart()
            if self._end == None or self._end < component.getEnd():
                self._end =  component.getEnd()
            self._diff = (self._end - self._start).days + 1

            self._children.sort(key=lambda x: x.getStart())

    def format(self, verbose=False):
        if self._price != 0 or verbose:
            text = "%s+ %s -> %s (%d)\t [%.2f]\n" % ('   '*self._deep, date_utils.format(self._start), date_utils.format(self._end), self._diff, self._price)
            for child in self._children:
                text += child.format(verbose)
        else:
            text = ''
        return text

    def getChildren(self):
        return self._children

    def isLeaf(self):
        return False

class Price(Component):
    def __init__(self, start, end, price, descr, color='white', attrs=None):
        self._start = start
        self._end = end
        self._diff = (end - start).days + 1
        self._price = price
        self._descr = descr
        self._deep = 0
        self._color = color
        self._attrs = attrs

    def format(self, verbose=False):
        if self._price != 0 or verbose:
            return "%s| %s -> %s (%d)\t [%.2f] %s\n" % ('   '*(self._deep), date_utils.format(self._start), date_utils.format(self._end), self._diff, self._price, color(self._descr, fg='green'))
        return ''

    def getChildren(self):
        return None

    def isLeaf(self):
        return True

    def getDescr(self):
        return self._descr

    def getColor(self):
        return self._color

    def getColorAttrs(self):
        return self._attrs
