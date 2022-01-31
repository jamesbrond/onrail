from datetime import datetime, timedelta

def explode(dates):
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
	return d.replace(day=1)

def first_day_of_week(d):
	return d + timedelta(days = -d.weekday())

def format(d):
	return d.strftime("%Y-%m-%d")

def is_workday(d, workdays):
	return d.weekday() in workdays

def last_day_of_month(d):
	next_month = d.replace(day=28) + timedelta(days=4)
	return next_month - timedelta(days=next_month.day)

def last_day_of_week(d):
	return d + timedelta(days=6 - d.weekday())

def now():
	return datetime.today()

def str2date(s):
	return datetime.strptime(s, '%Y-%m-%d').date()

def min(d1, d2):
	return d1 if d1 < d2 else d2

def max(d1, d2):
	return d1 if d1 > d2 else d2

# ~@:-]