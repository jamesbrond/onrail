"""
OnRail: la dura vita del pendolare è resa un po' meno dura dallo smartwork, ma
a quale prezzo? Calcola se conviene fare l'abbonamento o prendere biglietti
singoli in base ai giorni di smartwork, ferie, festività e trasferte.
"""

import sys
import logging
import argparse
import traceback
from lib import fndate
from lib.fare import Fare, ANNUALLY
from lib.config import Config
from lib.cal import CalendarExport


def main():
    """Entry function"""
    try:
        args = _parse_cmd_line()
        conf = Config(args)
        logging.basicConfig(
            level=conf['loglevel'],
            format="%(asctime)s %(levelname)s:%(name)s %(message)s",
            filename='onrail.log'
        )
        logging.debug("Configuration parameters: %s", conf)

        fares = Fare(conf)
        prices = fares.price(conf['start'], conf['end'], ANNUALLY)
        print(prices.format())

        if conf['show_calendar']:
            cal = CalendarExport(prices)
            cal.to_json()

        return 0
    except Exception as ex:
        print("ERROR: " + str(ex), file=sys.stderr)
        traceback.print_exc()
    return 1


def _date_type(value):
    try:
        return fndate.str2date(value)
    except Exception as ex:
        raise argparse.ArgumentTypeError("Fatal: invalid date") from ex


def _parse_cmd_line():
    parser = argparse.ArgumentParser(
        prog="OnRail",
        usage='%(prog)s [options]',
        description='Useless program for poor commuters.')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 2.0')
    parser.add_argument(dest='config',
                        type=argparse.FileType('r', encoding='utf8'),
                        help='YAML configuration file')
    parser.add_argument('--verbose', '-v',
                        action='store_const',
                        const=logging.DEBUG,
                        default=logging.ERROR)
    parser.add_argument('-s --start',
                        type=_date_type,
                        dest='start',
                        default=fndate.date_format(fndate.now()),
                        help='Start period date. Default today')
    parser.add_argument('-e --end',
                        type=_date_type,
                        dest='end',
                        help='End period date. Default end of start date month')
    parser.add_argument('--calendar',
                        dest='show_calendar',
                        action='store_true',
                        default=False,
                        help='Show calendar in browser')

    return vars(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
