# frost-client

[![Build Status](https://travis-ci.org/BergensTidende/frost-client.svg?branch=master)](https://travis-ci.org/BergensTidende/frost-client)

[![Documentation Status](https://readthedocs.org/projects/frost-client/badge/?version=latest)](https://frost-client.readthedocs.io/en/latest/?badge=latest)

This Python client wraps the [Frost API](https://frost.met.no/concepts#getting_started). You should 
read up on those docs before using this client. And be sure to check out met.no's 
[Terms of Use](https://frost.met.no/termsofuse)

The main purpose of this client is returns Pandas Dataframes from Frost API data.

This is an unofficial client. We have no relationship to met.no

Documentation: https://frost-client.readthedocs.io/en/latest/

## Install

Requires Python 3.7

`pip install frost-client`

or

`pipenv install frost-client`

This will install the frost-client and Pandas.

## Usage

The Frost API key should be exposed as a environment variable:

`FROST_API_KEY=xxxxxx` 

or passed as a username parameter when creating and instance of the class.

### Get weather data sources

Get all available observation sources (stations) for Hordaland county (12)

```
from frost.client import APIError, Frost
f = Frost()
res = f.get_sources(county='12')

# return as Pandas Dataframe
df = res.to_df()

# return IDs of sources as list
ids = res.to_ids_list()
```

### Get available time series

Display available time series for a station (here Bergen - Florida)

```
from frost.client import APIError, Frost
f = Frost()
res = f.get_available_timeseries(sources=['SN50540'])

# return as Pandas Dataframe
df = res.to_df()

```

### Get observations

Display observations for a station (here Bergen - Florida)

```
from frost.client import APIError, Frost
f = Frost()
res = f.get_observations(
            sources=['SN50540'],
            elements=['sum(precipitation_amount P1D)'],
            timeoffsets=['PT6H'],
            referencetime='2018-01-01/2018-02-01')
df = res.to_df()

```

See tests for more examples.

## Local development

You should use pipenv

### Tests

Enable the pipenv with

`pipenv shell`

Make sure to export env variable 

`FROST_API_KEY=xxxxxx`

To run all tests: 

`nosetests`

To run specific tests:

`nosetests tests.test_requests:TestFrostRequests.test_get_sources`
