from datetime import timedelta
from dateutil import relativedelta
import holidays
from pprint import pprint
from config import Config
from price import Prices, Price
import date_utils
from cal import Cal
from termcolor import colored

class Fare:

    def __init__(self):
        conf = Config();
        start= date_utils.str2date(conf.get('start'))
        end = date_utils.str2date(conf.get('end'))

        self._workdays = conf.get('workdays')
        self._exceptions = conf.getExceptions()
        self._business_exceptions = conf.getBusinessexceptions()

        prices = self.best(start, end, [conf.get('subscription_annual'), conf.get('subscription_monthly'), conf.get('subscription_weekly'), conf.get('ticket')], conf.get('smartwork'), 0)
        cal = Cal(prices, int(conf.get('firstweekday')))
        print('Best solution:')
        cal.prCalendar(w=int(conf.get('day_width')), l=int(conf.get('line_height')), c=int(conf.get('months_space')), m=int(conf.get('months_per_line')))
        print('Legend:')
        print('%s\n%s\n%s' % (colored('vacation', 'red'), colored('out of office', 'blue'), colored('smartwork', 'magenta')))
        print('%s\n%s\n%s' % (colored('daily ticket', 'white'), colored('weekly subscription', 'green'), colored('monthly subscription', 'cyan')))
        print('\nDetails:')

        print(prices.format(conf.get('verbose')))

    def daily(self, start, end, price, smartwork):
        sw = smartwork
        d = start;
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
                    if sw > 0:
                        coverage.append(Price(d, d, 0, 'smartwork [sw %d]' % (smartwork), 'magenta'))
                    else:
                        coverage.append(Price(d, d, price*2, 'daily ticket [sw %d]' % (smartwork)))
                    sw -= 1
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
            coverage.append(Price(d, d + relativedelta.relativedelta(months=1, days=-1), price, 'monthly subscription', 'cyan'))
            d += relativedelta.relativedelta(months=1)
        return coverage

    def annually(self, start, end, price):
        d = e = start
        while end > e:
            e += relativedelta.relativedelta(years=1, days=-1)
        coverage = Prices();
        while d < e:
            coverage.append(Price(d, d + relativedelta.relativedelta(years=1, days=-1), price, 'annual subscription', 'white', ['underline']))
            d += relativedelta.relativedelta(years=1)
        return coverage

    def best(self, start, end, prices, smartwork, deep):
        #print("%s deep %d: analyzing periond: %s -> %s" % ('   '*deep, deep, date_utils.format(start), date_utils.format(end)))
        if deep == 0:
            p0 = self.annually(start, end, prices[deep])
        elif deep == 1:
            p0 = self.monthly(start, end, prices[deep])
        elif deep == 2:
            p0 = self.weekly(start, end, prices[deep])
        elif deep == 3:
            return self.daily(start, end, prices[deep], smartwork)

        coverage = Prices();
        for period in p0.getChildren():
            p1 = self.best(max(start, period.getStart()), min(end, period.getEnd()), prices, smartwork, deep + 1)
            if p1.getPrice() < period.getPrice():
                #print('%s wins on %s' % (p1.getPrice(), period.getPrice()))
                if deep == 2:
                    p2 = p1
                    sw = smartwork
                    while p2.getPrice() < period.getPrice() and sw > 0:
                        p1 = p2
                        sw -= 1
                        p2 = self.best(max(start, period.getStart()), min(end, period.getEnd()), prices, sw, deep + 1)
                coverage.append(p1)
            else:
                #print('%s wins on %s' % (period.getPrice(), p1.getPrice()))
                coverage.append(period)
        return coverage
