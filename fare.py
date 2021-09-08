from datetime import timedelta
from dateutil import relativedelta
import holidays
from config import Config
from price import Prices, Price
import date_utils
from cal import Cal
from colors import color
from time import strftime
import sys

class Fare:

    def __init__(self):
        conf = Config()
        self.logger = conf.get_logger()

        try:
            start = date_utils.str2date(conf.get('start'))
        except Exception:
            self.logger.error("Fatal: invalid start date", exc_info=True)
            print("Fatal: invalid start date", file=sys.stderr)
            sys.exit(1)
        try:
            end = date_utils.str2date(conf.get('end'))
        except Exception:
            print("Fatal: invalid end date", file=sys.stderr)
            self.logger.error("Fatal: invalid end date", exc_info=True)
            sys.exit(1)

        if start > end:
            print("Fatal: end date must be after than start date", file=sys.stderr)
            self.logger.error("Fatal: end date must be after than start date")
            sys.exit(1)

        self._workdays = conf.get('workdays')
        self._exceptions = conf.getExceptions()
        self._business_exceptions = conf.getBusinessexceptions()

        prices = self.best(start, end, [conf.get('prices', 'subscription_annual'), conf.get('prices', 'subscription_monthly'), conf.get('prices', 'subscription_weekly'), conf.get('prices', 'ticket')], conf.get('homeoffice'), 0)
        cal = Cal(prices, int(conf.get('firstweekday')))
        print(color(f" Best solution [ { date_utils.format(start)} - {date_utils.format(end)} ]:", style='bold') + "\n")
        if conf.get('show_calendar'):
            cal.formatCalendar(c=conf.get('months_space'), m=conf.get('months_per_line'))
            car = ' '
            print(f"{color('Legend', style='bold')}: {color(car, bg='red')} vacation, {color(car, bg='blue')} out of office, {color(car, bg='magenta')} home office, {color(car, bg='white')} daily ticket, {color(car, bg='green')} weekly subscription, {color(car, bg='cyan')} monthly subscription")
            print('\n')
        print(prices.format(conf.get('verbose')))

    def daily(self, start, end, price, homeoffice):
        ho = homeoffice
        d = start
        exceptions = self._exceptions
        business_exceptions = self._business_exceptions
        holid = holidays.IT(years=start.year)
        for date, name in sorted(holid.items()):
            exceptions.append(date)

        coverage = Prices()
        while d <= end:
            if date_utils.isWorkday(d, self._workdays):
                if d in exceptions:
                    coverage.append(Price(d, d, 0, 'vacation', 'red'))
                elif d in business_exceptions:
                    coverage.append(Price(d, d, 0, 'out of office', 'blue'))
                else:
                    if ho > 0:
                        coverage.append(Price(d, d, 0, 'home office [ho %d]' % (homeoffice), 'magenta'))
                    else:
                        coverage.append(Price(d, d, price*2, 'daily ticket [ho %d]' % (homeoffice)))
                    ho -= 1
            else:
                coverage.append(Price(d, d, 0, '', 'red'))
            d += timedelta(days=1)
        return coverage

    def weekly(self, start, end, price):
        d = date_utils.firstDayOfWeek(start)
        e = date_utils.lastDayOfWeek(end)
        coverage = Prices()
        while d < e:
            coverage.append(Price(d, d + timedelta(days=6), price, 'weekly subscription', 'green'))
            d += timedelta(days=7)
        return coverage

    def monthly(self, start, end, price):
        d = date_utils.firstDayOfMonth(start)
        e = date_utils.lastDayOfMonth(end)
        coverage = Prices()
        while d < e:
            coverage.append(Price(d, d + relativedelta.relativedelta(months=1, days=-1), price, f"{d.strftime('%B')} monthly subscription", 'cyan'))
            d += relativedelta.relativedelta(months=1)
        return coverage

    def annually(self, start, end, price):
        d = e = start
        while end > e:
            e += relativedelta.relativedelta(years=1, days=-1)
        coverage = Prices()
        while d < e:
            coverage.append(Price(d, d + relativedelta.relativedelta(years=1, days=-1), price, 'annual subscription', 'white', ['underline']))
            d += relativedelta.relativedelta(years=1)
        return coverage

    def _best_init(self, deep, start, end, prices):
        if deep == 0:
            return self.annually(start, end, prices[deep])
        elif deep == 1:
            return self.monthly(start, end, prices[deep])
        elif deep == 2:
            return self.weekly(start, end, prices[deep])


    def best(self, start, end, prices, homeoffice, deep):
        if deep == 3:
            return self.daily(start, end, prices[deep], homeoffice)

        p0 = self._best_init(deep, start, end, prices)

        coverage = Prices()
        for period in p0.getChildren():
            p1 = self.best(max(start, period.getStart()), min(end, period.getEnd()), prices, homeoffice, deep + 1)
            if p1.getPrice() < period.getPrice():
                if deep == 2:
                    p2 = p1
                    ho = homeoffice
                    while p2.getPrice() < period.getPrice() and ho > 0:
                        p1 = p2
                        ho -= 1
                        p2 = self.best(max(start, period.getStart()), min(end, period.getEnd()), prices, ho, deep + 1)
                coverage.append(p1)
            else:
                coverage.append(period)
        return coverage

# ~@:-]