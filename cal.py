import calendar
from dateutil import relativedelta
from termcolor import colored
import date_utils

class Cal(calendar.TextCalendar):
    def __init__(self, prices, firstweekday=0):
        super().__init__(firstweekday)
        self._prices = prices
        self._start = prices.getStart();
        self._end = prices.getEnd();

    def getLeaves(self, prices):
        leaves = []
        for child in prices.getChildren():
            if child.isLeaf():
                leaves.append(child)
            else:
                ll = self.getLeaves(child)
                leaves.extend(ll)
        return leaves

    def formatCalendar(self, w=2, l=1, c=6, m=3):
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append

        leaves = self.getLeaves(self._prices)
        colors = {}
        for leaf in leaves:
            strrange = '%s -> %s' % (date_utils.format(leaf.getStart()), date_utils.format(leaf.getEnd()))
            for date in date_utils.explodeDates([strrange]):
                colors[date_utils.format(date)] = (leaf.getColor(), leaf.getColorAttrs())

        header = self.formatweekheader(w)
        d = self._start
        while d < self._end:
            theyear = d.year
            themonth = d.month
            if theyear == self._end.year:
                months = range(themonth, min(m + themonth, self._end.month+1))
            elif m + themonth > 13:
                months = [i for j in (range(themonth, 13), range(1,  m + 12 - themonth)) for i in j]
            else:
                months = range(themonth, m + themonth)
            names = (self.formatmonthname(theyear, k, 7 * (w + 1) - 1) for k in months)
            a(colored(self.formatstring(names, colwidth, c), 'white', attrs=['reverse']))
            a('\n'*l)
            headers = (header for k in months)
            a(colored(self.formatstring(headers, colwidth, c).rstrip(), 'white', attrs=['bold']))
            a('\n'*l)
            cal = []
            for k in months:
                cal.append(self.monthdatescalendar(theyear, k))
            height = max(len(wks) for wks in cal)
            for j in range(height):
                weeks = []
                for k in range(len(months)):
                    if j >= len(cal[k]):
                        weeks.append('')
                    else:
                        weeks.append(self.formatweekWithColor(cal[k][j], w, colors))
                a(self.formatstring(weeks, colwidth, c).rstrip())
                a('\n' * l)

            d += relativedelta.relativedelta(months=m)
        return ''.join(v)

    def prCalendar(self, w=2, l=1, c=6, m=3):
        print(self.formatCalendar(w, l, c, m))

    def formatweekWithColor(self, theweek, width, colors):
        return ' '.join(self.formatdayWithColor(d, width, colors) for (d) in theweek)

    def formatdayWithColor(self, d, width, colors):
        day = d.day
        df =  date_utils.format(d);
        if df in colors:
            color = colors[df][0]
            attrs = colors[df][1]
        else:
            color = 'grey'
            attrs = None
        if day == 0:
            s = ''
        else:
            s = colored('%2i' % day, color=color, attrs=attrs)
        return s.center(width)

    def formatstring(self, cols, colwidth=(7*3 - 1) , spacing=6):
        spacing *= ' '
        return spacing.join(c.center(colwidth) for c in cols)
