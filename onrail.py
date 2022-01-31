import os
import sys
import logging
import argparse
import traceback
from lib import fndate
from lib.fare import Fare, ANNUALLY
from lib.config import Config

def parse_cmd_line():
	parser = argparse.ArgumentParser(
		prog="OnRail",
		usage='%(prog)s [options]',
		description='Useless program for poor commuters.')

	parser.add_argument('--version', action='version', version='%(prog)s 2.0')
	parser.add_argument(dest='config', type=argparse.FileType('r', encoding='utf8'), help='YAML configuration file')
	parser.add_argument('--verbose', '-v', action='count', default=0)
	parser.add_argument('-s --start', dest='start', default=fndate.format(fndate.now()), help='Start period date. Default today')
	parser.add_argument('-e --end', dest='end', help='End period date. Default end of start date month')
	parser.add_argument('--calendar', dest='show_calendar', action='store_true', default=False, help='Show calendar')

	return vars(parser.parse_args())

def main():
	try:
		args = parse_cmd_line()
		conf = Config(args)
		logging.basicConfig(
			level=conf['loglevel'],
			format="%(asctime)s %(levelname)s:%(name)s %(message)s",
			filename=os.path.join('log', 'onrail.log')
		)
		logging.debug(f"Configuration parameters: {conf}")

		fares = Fare(conf)
		prices = fares.price(conf['start'], conf['end'], ANNUALLY)
		print(prices.format())

		if conf["show_calendar"]:
			from lib.cal import CalendarExport
			cal = CalendarExport(prices)
			cal.to_json()


		return 0
	except Exception as e:
		print("ERROR: " + str(e), file=sys.stderr)
		traceback.print_exc()
	return 1

if __name__ == "__main__":
	sys.exit(main())

# ~@:-]
