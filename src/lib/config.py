"""Configuration parser"""

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from lib import fndate


EXCEPTION_KEYS = ['full day leave', 'holiday', 'travel', 'smartwork']


class ExceptionDateList:
    """List of exceptions"""

    def __init__(self):
        self._date_list = []
        self._dscr_list = []

    def add(self, date, dscr=''):
        """Add"""
        self._date_list.append(date)
        self._dscr_list.append(dscr)

    def extend(self, dates, dscr):
        """Extend"""
        for d in dates:
            self.add(d, dscr)

    def __contains__(self, o):
        return o in self._date_list

    def __len__(self):
        return self._date_list.__len__()

    def __iter__(self):
        return self._date_list.__iter__()

    def __getitem__(self, d):
        return self._dscr_list[self._date_list.index(d)]

    def __str__(self):
        items = dict(zip(self._date_list, self._dscr_list))
        return f"[{', '.join([f'{{date: {k}, description: {v}}}' for k,v in items.items()])}]"


class Config(dict):
    """Configuration class"""

    def __init__(self, args):
        self['start'] = args['start']

        try:
            if "end" not in args or args['end'] is None:
                self['end'] = fndate.last_day_of_month(self['start'])
            else:
                self['end'] = args['end']
        except Exception as ex:
            raise ValueError("Fatal: invalid end date") from ex

        if self['start'] > self['end']:
            raise ValueError("Fatal: end date must be after than start date")

        self['show_calendar'] = args['show_calendar']
        self['loglevel'] = args['verbose']

        with args['config'] as file:
            self.update(load(file, Loader=Loader))

        self['exceptions'] = ExceptionDateList()
        for key in self['calendar']:
            if key in EXCEPTION_KEYS:
                self['exceptions'].extend(self._add_exception(key), key)

    def _add_exception(self, key):
        return fndate.explode([x.strip() for x in self['calendar'][key].split(',')])

# ~@:-]
