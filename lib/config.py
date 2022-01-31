from lib import fndate
from yaml import load
try:
  from yaml import CLoader as Loader
except ImportError:
  from yaml import Loader

class Config(dict):
	def __init__(self, args):
		try:
			self['start'] = fndate.str2date(args['start'])
		except Exception:
			raise ValueError("Fatal: invalid start date")

		try:
			if "end" not in args or args['end'] is None:
				self['end'] = fndate.last_day_of_month(self['start'])
			else:
				self['end'] = fndate.str2date(args['end'])
		except Exception:
			raise ValueError("Fatal: invalid end date")

		if self['start'] > self['end']:
			raise ValueError("Fatal: end date must be after than start date")

		self['show_calendar'] = args['show_calendar']
		self['loglevel'] = (args['verbose'] - 4) * -10

		with args['config'] as file:
			self.update(load(file, Loader=Loader))

		self['exceptions'] = []
		for key in self['calendar']:
			if key == 'vacations' or key == 'holidays' or key == 'travels':
				self['exceptions'].extend(fndate.explode([x.strip() for x in self['calendar'][key].split(',')]))

# ~@:-]