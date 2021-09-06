import os
import logging
import argparse
import date_utils
import yaml

class Config:
    'Defines what arguments it requires, and figures out how to parse those out of sys.argv.'

    def __init__(self):
        parser = argparse.ArgumentParser(prog="OnRail", usage='%(prog)s [options]', description='Useless program for poor commuters.')
        parser.add_argument('--version', action='version', version='%(prog)s 1   .0')
        parser.add_argument('-c', '--config', dest='config', required=True, help='Use the file ad configuration')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Produce a more verbose output')
        parser.add_argument('--debug', dest='debug', action='store_true', help='Writes debug informations to onrail.log file')
        parser.add_argument('-s --start', dest='start', default=date_utils.format(date_utils.now()), help='Start period date. Default today')
        parser.add_argument('-e --end', dest='end', help='End period date. Default end of start date month')
        parser.add_argument('--calendar', dest='show_calendar', action='store_true', default=False, help='Show calendar')
        args = vars(parser.parse_args())
        end = args.get('end')
        if not end:
            args['end'] = date_utils.format(date_utils.lastDayOfMonth(date_utils.str2date(args['start'])))

        with open(args['config'], 'r') as file:
            self._config = yaml.safe_load(file)

        self._exceptions = []
        self._business_exceptions = []
        for key in self._config['calendar']:
            if key == 'vacations' or key == 'holidays':
                self._exceptions.extend(date_utils.explodeDates([x.strip() for x in self._config['calendar'][key].split(',')]))
            elif key == 'travels':
                self._business_exceptions.extend(date_utils.explodeDates([x.strip() for x in self._config['calendar'][key].split(',')]))

        self._logger = self.getLogger()
        for key in args:
            val = args[key]
            if (val != None):
                    self._logger.debug(f"{key} => {val}")
                    self._config[key] = val

    def get(self, *args):
        if len(args) == 1:
            return self._config[args[0]]
        else:
            return self._config[args[0]][args[1]]

    def getExceptions(self):
        return self._exceptions

    def getBusinessexceptions(self):
        return self._business_exceptions

    def getLogger(self):
        name = self._config['logger']['log_name'].replace('.log', '')
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            file_name = os.path.join(self._config['logger']['log_dir'], '%s.log' % name)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            if self._config['logger']['debug']:
                handler.setLevel(logging.DEBUG)
            else:
                handler.setLevel(logging.ERROR)
            logger.addHandler(handler)
        return logger
