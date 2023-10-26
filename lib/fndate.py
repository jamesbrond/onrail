"""
Date and time functions
"""
from datetime import datetime, timedelta


def explode(dates):
    """Explodes date range"""
    results = []
    for date in dates:
        if '->' in date:
            date_range = [x.strip() for x in date.split('->')]
            d = str2date(date_range[0])
            e = str2date(date_range[1])
            while d <=e:
                results.append(d)
                d += timedelta(days=1)
        else:
            results.append(str2date(date))
    return results


def first_day_of_month(d):
    """First day of the month"""
    return d.replace(day=1)


def first_day_of_week(d):
    """First day of the week"""
    return d + timedelta(days = -d.weekday())


def date_format(d):
    """Date to YYYY-MM-DD format"""
    return d.strftime("%Y-%m-%d")


def is_workday(d, workdays):
    """Return true if day is a work day"""
    return d.weekday() in workdays


def last_day_of_month(d):
    """Last day of the month"""
    next_month = d.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def last_day_of_week(d):
    """Last day of the week"""
    return d + timedelta(days=6 - d.weekday())


def now():
    """Today"""
    return datetime.today()


def str2date(s):
    """String to date"""
    return datetime.strptime(s, '%Y-%m-%d').date()


def date_min(d1, d2):
    """Return the earliest of the two dates"""
    return d1 if d1 < d2 else d2


def date_max(d1, d2):
    """Return the major date"""
    return d1 if d1 > d2 else d2

# ~@:-]
