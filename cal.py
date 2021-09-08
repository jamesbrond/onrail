import calendar
from dateutil import relativedelta
from colors import color

import date_utils
import math

class Cal(calendar.TextCalendar):
    def __init__(self, prices, firstweekday=0):
        super().__init__(firstweekday)
        self._prices = prices
        self._start = prices.getStart()
        self._end = prices.getEnd()

    def getLeaves(self, prices):
        leaves = []
        for child in prices.getChildren():
            if child.isLeaf():
                leaves.append(child)
            else:
                ll = self.getLeaves(child)
                leaves.extend(ll)
        return leaves

    # @param w day width
    # @param l line height
    # @param c months space
    # @param m months_per_line
    def formatCalendar(self, c=6, m=3):
        w = 2
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1 # day_width + space * 7 - trailing space

        leaves = self.getLeaves(self._prices)
        colors = {}
        for leaf in leaves:
            strrange = '%s -> %s' % (date_utils.format(leaf.getStart()), date_utils.format(leaf.getEnd()))
            for date in date_utils.explodeDates([strrange]):
                colors[date_utils.format(date)] = (leaf.getColor(), leaf.getColorAttrs())


        r = relativedelta.relativedelta(date_utils.firstDayOfMonth(self._end), date_utils.firstDayOfMonth(self._start))
        month_tot = r.years * 12 + r.months + 1
        month_lines = math.ceil(month_tot / m)
        d = self._start
        for i in range(month_lines):
            month_rows = min(m, month_tot - m*i)
            rows = ["" for k in range(7)]
            for j in range(month_rows):
                rows[0] += f"{color(self.formatmonthname(d.year, d.month, colwidth), fg='white', bg='blue', style='bold')}{' ' * c}"
                rows[1] += f"{color(self.formatweekheader(w), fg='black', bg='white', style='bold')}{' ' * c}"
                month_calendar = self.monthdatescalendar(d.year, d.month)
                for k in range(len(month_calendar)):
                    for month_day in month_calendar[k]:
                        rows[k + 2] += f"{self.formatdayWithColor(month_day, w, colors)} "
                    rows[k + 2] += " " * (c -1)
                d += relativedelta.relativedelta(months=1)

            for row in rows:
                print(row)
            print("\n")


    def formatdayWithColor(self, d, width, colors):
        df =  date_utils.format(d)
        day = d.day
        if df in colors:
            return color(f"{'%2s' % day}", fg=colors[df][0], style=colors[df][1])
        else:
            return f"{'%2s' % day}"
