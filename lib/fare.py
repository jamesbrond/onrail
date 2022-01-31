import holidays
from lib import fndate
from datetime import timedelta
from dateutil import relativedelta
from lib.price import Price, Prices

ANNUALLY = 0
MONTHLY  = 1
WEEKLY   = 2
DAILY    = 3

_ticket2number = {
	'ticket': DAILY,
	'subscription_weekly': WEEKLY,
	'subscription_monthly': MONTHLY,
	'subscription_annual': ANNUALLY
}

class Fare:
	def __init__(self, conf) -> None:
		self.workdays = conf['workdays']
		self.exceptions = conf['exceptions']
		self.holidays = conf['holidays']
		self.homeoffice = conf['homeoffice']
		self.prices = [0, 0, 0, 0]
		for s in conf['prices']:
			self.prices[_ticket2number[s]] = conf['prices'][s]

	def price(self, start, end, deep):
		parent = self._price_init(start, end, deep)
		if deep == DAILY or len(parent) == 0:
			return parent
		coverage = Prices()
		for child in parent.get_children():
			s = max(start, child.start())
			e = min(end, child.end())
			deeper = self.price(s, e, deep + 1)
			coverage.append(deeper if deeper.price() < child.price() else child)
		return coverage

	def _price_init(self, start, end, deep):
		return {
			ANNUALLY: self.annually(start, end),
			MONTHLY: self.monthly(start, end),
			WEEKLY: self.weekly(start, end),
			DAILY: self.daily(start, end)
		}.get(deep)

	def annually(self, start, end):
		price = self.prices[ANNUALLY]
		d = e = start
		while end > e:
			e += relativedelta.relativedelta(years=1, days=-1)
		coverage = Prices()
		while d < e:
			coverage.append(Price(d, d + relativedelta.relativedelta(years=1, days=-1), price, 'annually subscription', 'annual'))
			d += relativedelta.relativedelta(years=1)
		return coverage

	def monthly(self, start, end):
		price = self.prices[MONTHLY]
		d = fndate.first_day_of_month(start)
		e = fndate.last_day_of_month(end)
		coverage = Prices()
		while d < e:
			coverage.append(Price(d, d + relativedelta.relativedelta(months=1, days=-1), price, f"{d.strftime('%B')} monthly subscription", 'monthly'))
			d += relativedelta.relativedelta(months=1)
		return coverage

	def weekly(self, start, end):
		price = self.prices[WEEKLY]
		d = fndate.first_day_of_week(start)
		e = fndate.last_day_of_week(end)
		coverage = Prices()
		while d < e:
			coverage.append(Price(d, d + timedelta(days=6), price, 'weekly subscription', 'weekly'))
			d += timedelta(days=7)
		return coverage

	def daily(self, start, end):
		price = self.prices[DAILY]
		exceptions = self.exceptions
		holid = {}
		for i in range(start.year, end.year + 1):
			holid.update(eval(f"holidays.{self.holidays}")(years=i))
		for h, name in sorted(holid.items()):
			exceptions.append(h)
		d = start
		ho = self.homeoffice - d.weekday()
		coverage = Prices()
		while d <= end:
			if fndate.is_workday(d, self.workdays):
				if d in exceptions:
					coverage.append(Price(d, d, 0, 'no office', 'daily'))
				else:
					if ho > 0:
						coverage.append(Price(d, d, 0, f"home office (ho {self.homeoffice})", 'daily'))
						ho -= 1
					else:
						coverage.append(Price(d, d, price*2, f"daily ticket (ho {self.homeoffice})", 'daily'))
			else:
				coverage.append(Price(d, d, 0, '', 'daily'))
				ho = self.homeoffice
			d += timedelta(days=1)

		return coverage

# ~@:-]