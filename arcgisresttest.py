__author__ = 'James'

import timeit
import inspect
import urlparse
import urllib
import urllib2
import json
import time


def get_24hr_time():
    return time.strftime("%H:%M:%S")

def get_date():
    return time.strftime("%x")

## Pass function object, args as dict, number of repeats int, and mode (min, max, mean, stdev)
def time_function(function, functionArguments, repeats, mode='mean'):

    ## Check to make sure all arguments for timeCall are valid
    if not hasattr(function, '__call__'):
        raise ValueError("First argument is not a function")
    if not isinstance(functionArguments, dict):
        raise ValueError("Second argument is not dictionary")
    elif isinstance(functionArguments, list):
        for arg, param in functionArguments.iteritems():
            if not isinstance(arg, str) or not isinstance(param, str):
                raise ValueError(arg,"or", param, "is not a string, or can not be coerced")
    if not isinstance(repeats, int):
        raise ValueError("Number of repeats is not an interger")

    ## Setup the function
    functionParams = inspect.getargspec(function).args
    if len(functionParams) > len(functionArguments):
        raise TypeError('Too many arguments for specified function!')
    else:
        kwParams = [arg + "='" + param + "'" for arg, param in functionArguments.iteritems()]
        functionName = function.func_name
        functionArgumentsStr = ",".join(kwParams)

        functionCall = functionName + "(" + functionArgumentsStr + ")"
        functionImport = "from __main__ import " + functionName
        print("Running the following function: " + functionCall)
        timer = timeit.Timer(functionCall, functionImport)
        times = timer.repeat(repeats, 1)
        return time_return_type(times, mode)


def time_code(code, repeats, mode='mean'):
    """Return mean of list items"""
    if not isinstance(code, str):
        raise ValueError("Code of is not an string")
    if not isinstance(repeats, int):
        raise ValueError("Number of repeats is not an string")

    timer = timeit.Timer(code)
    times = timer.repeat(repeats, 1)
    return time_return_type(times, mode)

def time_return_type(times, mode):
    """Define the return type for code timings"""
    if mode == 'mean':
        return mean(times)
    elif mode == 'min':
        return min(times)
    elif mode == 'max':
        return max(times)
    elif mode == 'stdev':
        return stdev(times)
    else:
        raise ValueError("Mode not valid: mean, min, max or stdev allowed")

def mean(items):
    """Return mean of list items"""
    sum = 0
    for elm in items:
        sum += elm
    return sum/(len(items)*1.0)

def sum_of_squaredevs(data):
    """Return sum of square deviations of list items"""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = sum_of_squaredevs(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def check_url(url):
    if not isinstance(url, str):
        raise ValueError("URL is not a string!")

def check_params(url, params):
    if not isinstance(params, dict):
        raise ValueError("URL parameter is not a dictionary")
    if query_params_to_dict(url) != {}:
        raise ValueError("URL already has parameters in string, place in parameter argument")

def request_json(url, params={'f':'json'}):
    check_url(url)
    check_params(url, params)
    if params:
        url += "?" + urllib.urlencode(params)
    response = urllib2.urlopen(url)
    jsonpayload = json.load(response)
    return jsonpayload

def request_html(url, params={'f':'html'}):
    check_url(url)
    check_params(url, params)
    if params:
        url += "?" + urllib.urlencode(params)
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def dict_to_str(dict):
    return json.dumps(dict)

def get_base_url(url):
    url_split = urlparse.urlsplit(url)
    return '{url.scheme}://{url.netloc}/'.format(url=url_split)

def get_fullpath_url(url):
    url_split = urlparse.urlsplit(url)
    return '{url.scheme}://{url.netloc}{url.path}'.format(url=url_split)

def query_params_to_dict(url):
    params = urlparse.parse_qs(urlparse.urlsplit(url).query)
    for k, v in params.iteritems(): params[k] = params[k][0]
    return params

def dict_to_query_string(dict):
    return urllib.unquote(urllib.urlencode(dict))


## ArcGIS Specific Functions

## Get app token
def get_arcgis_app_token(client_id, client_secret, expiration):
    params={
      'f': 'json',
      'client_id': client_id,
      'client_secret': client_secret,
      'grant_type': 'client_credentials',
      'expiration': expiration
    }
    return request_json('https://www.arcgis.com/sharing/rest/oauth2/token/', params )['access_token']



## Feature Service (and similar) related functions
def get_service_views(url):
    jsonpayload = request_json(url)
    try:
        return jsonpayload["numViews"]
    except KeyError:
        print "numViews was not found in the json payload"

def get_service_size(url):
    jsonpayload = request_json(url)
    try: 
        return jsonpayload["size"]
    except KeyError:
        print "Size was not found in the json payload"

def get_service_type(url):
    jsonpayload = request_json(url)
    try: 
        return jsonpayload["type"]
    except KeyError:
        print "Type was not found in the json payload"

def get_service_name(url):
    jsonpayload = request_json(url)
    try: 
        return jsonpayload["name"]
    except KeyError:
        print "Name was not found in the json payload"

def get_service_formats(url):
    jsonpayload = request_json(url)
    try:
        return jsonpayload["supportedQueryFormats"]
    except KeyError:
        print "Supported foramts were not found in the json payload"

#def get_cost_of_service(url):

    #costDetails = [1024*1024*1024, 1.2, "file"]         # file -> 1.2 credits/GB/month
    ##if item['type'] == 'Feature Service':
        ##costDetails = [1024*1024*10, 2.4, "feature"]

#print get_service_name("http://services.arcgis.com/Qo2anKIAMzIEkIJB/arcgis/rest/services/TubeMap/FeatureServer/")



## USAGE

# t = time_function(get_arcgis_app_token, { 'client_id' : '', 'client_secret' : '','expiration' : '1440'}, 1, "mean")
#
# url = "http://services.arcgis.com/Qo2anKIAMzIEkIJB/arcgis/rest/services/TubeMap/FeatureServer/2?f=json"
# print(get_base_url(url))
# print(get_fullpath_url(url))
# print(dict_to_str({1:2}))
# print(query_params_to_dict(url))
# print(get_service_type(url))
# size = get_service_size(url)
# print size
# print(get_service_views(url))
# print(get_service_name(url))
#print(recode_url_to_string(url) )

#print(recode_url_to_string(url))
