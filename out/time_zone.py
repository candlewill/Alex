#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from datetime import datetime
import json

from out.apirequest import APIRequest
import calendar

from functools import lru_cache

class Time(object):
    pass


class GoogleTimeFinder(APIRequest):
    def __init__(self):
        APIRequest.__init__(self, 'openweathermap', 'OpenWeatherMap query')

    def obtain_geo_codes(self, place='New York'):
        """:
        :return: Returns tuple (longitude, latitude) for given place. Default value for place is New York
        """

        data = {'address': place, 'language': 'en'}
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        try:
            page = urlopen(url + urlencode(data))
        except HTTPError as e:
            print(e.code)
            return None, None
        else:
            json_obj = json.loads(str(page.read(), 'utf-8'))
            # print(json_obj)
            return [(result['geometry']['location']['lng'], result['geometry']['location']['lat']) for result in
                    json_obj['results']][0]

    @lru_cache(maxsize=8)
    def get_time(self, place=None, lat=None, lon=None):
        """Get time information at given place
        """

        # obtain longitude and latitude, if they are not set
        if lat is None and lon is None:
            lon, lat = self.obtain_geo_codes(place)
            print("The lon and lat of %s, is: %s, %s" % (place, lon, lat))
            # gaining geo location may fail
            if lat is None and lon is None:
                return None, None

        d = datetime.utcnow()
        timestamp = calendar.timegm(d.utctimetuple())
        data = {'location': str(lat) + ',' + str(lon),
                'timestamp': int(timestamp),
                'language': 'en'}

        self.system_logger.info("GoogleTime request:\n" + ' + ' + str(data))

        try:
            page = urlopen('https://maps.googleapis.com/maps/api/timezone/json?' + urlencode(data))
        except HTTPError as e:
            print(e.code)
            return None, None
        else:
            response = json.loads(str(page.read(), "utf-8"))
            self._log_response_json(response)
            time, time_zone = self.parse_time(response)
            self.system_logger.info("GoogleTime response:\n" + str(time) + "," + str(time_zone))
            return time, time_zone

    def parse_time(self, response):
        print(response)
        time_zone = response[u'timeZoneName']
        offset = response['rawOffset'] + response['dstOffset']
        d = datetime.utcnow()
        timestamp = calendar.timegm(d.utctimetuple())
        time = datetime.fromtimestamp(int(timestamp) + offset)
        # int(time.mktime(departure_time.timetuple()))
        print(time)
        return time, time_zone


if __name__ == '__main__':
    time = GoogleTimeFinder()
    cur_time, time_zone = time.get_time(place="Taipet")
    print(cur_time)
    print(time_zone)