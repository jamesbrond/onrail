from datetime import datetime, timedelta

def format(d):
    return d.strftime("%Y-%m-%d")

def firstDayOfMonth(day):
    return day.replace(day=1)

def firstDayOfWeek(day):
    return day + timedelta(days = -day.weekday())

def isWorkday(day, workdays):
    return day.weekday() in workdays

def lastDayOfMonth(day):
    next_month = day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def lastDayOfWeek(day):
    return day + timedelta(days=6 - day.weekday());

def min(d1, d2):
    if d1 < d2:
        return d1
    else:
        return d2

def max(d1, d2):
    if d1 > d2:
        return d1
    else:
        return d2

def now():
    return datetime.today();

def str2date(str):
    return datetime.strptime(str, '%Y-%m-%d').date()

def explodeDates(dates):
    results = []
    for date in dates:
        if '->' in date:
            range = [x.strip() for x in date.split('->')]
            d = str2date(range[0])
            e = str2date(range[1])
            while d <=e:
                results.append(d)
                d += timedelta(days=1)
        else:
            results.append(str2date(date))
    return results
