#!/usr/bin/python

import requests
import datetime

def flyby(latitude, longitude):
    """
    Sends HTTP GET request to NASA API to predict the next time a satellite image will
    be taken of a specified location.
    """
    # check for valid latitude and longitude
    if latitude > 90 or latitude < -90 or longitude > 180 or longitude < -180:
        print 'ERROR: Please input valid latitude and longitude'
        return

    url = 'https://api.nasa.gov/planetary/earth/assets'
    payload = {
        'lat': latitude,
        'lon': longitude,
        'api_key': 'INSERT_KEY'
    }
    r = requests.get(url, params=payload)
    # full json data of GET request
    data = r.json()

    # check request was successful
    if r.status_code is not 200:
        print 'ERROR: HTTP request returned incorrect status code of %d' % r.status_code
        print r.json()
        return
    # check that there is enough data in request
    if data['count'] < 2:
        print 'ERROR: NASA does not have enough data for specified location to make a prediction'
        return

    # parse unicode dates to datetime dates
    dates = [datetime.datetime.strptime(i['date'], '%Y-%m-%dT%H:%M:%S') for i in data['results']]
    # make sure dates are in order
    dates.sort()
    # compute times between each image
    deltas = [(dates[i + 1] - dates[i]) for i in range(0, len(dates) - 1)]
    # compute average of time between every image 
    avg_time_delta = sum(deltas, datetime.timedelta()) / len(deltas)

    # print out the next time (on average) an image should be recorded
    print 'Next time: ' + str(dates[len(dates)-1] + avg_time_delta)

flyby(90, 180)
flyby(-91, -79.34234)
flyby(43.078154, -79.075891)
