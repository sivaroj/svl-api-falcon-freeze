import os
import configparser


class ReadConf():
    def __init__(self):
        self.conf = None
        wk_dir = os.path.dirname(os.path.realpath(__file__))
        # file name must be 'config.ini'
        file_name = wk_dir + os.sep + 'config.ini'
        self.conf = configparser.ConfigParser()
        self.conf._interpolation = configparser.ExtendedInterpolation()
        self.conf.read(str(file_name), encoding='utf-8')  # if use unicode utf-8

    def here_map(self):
        return {'apiKey':  self.conf.get('here_map', 'apiKey'),
                'reverseGeocodeURL': self.conf.get('here_map', 'reverseGeocodeURL'),
                'routeURL': self.conf.get('here_map', 'routeURL'),
                'routeURLv8': self.conf.get('here_map','routeURLv8')}

    def Nostra_map(self):
        return {'token': self.conf.get('nostra_map', 'token'),
                'apiURL': self.conf.get('nostra_map', 'apiURL')}

