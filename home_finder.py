import pandas as pd
import requests


# Outline
# Inputs - Counties of Interest as List or Cities of Interest as a List, Home Filters [Minimum price, max price, foreclosure, bedrooms, bathrooms, etc...]
# 1. Check if counties have already been queried and remove them from the input list
# 2. Run Counties API to get cities from counties and append/save in a file
# 3. Run School API to get school districts ranks for new cities and append/save in a file
# 4. Run Commute API to get the commute score for new cities and append/save in a file
# 4. Run Realtor API to get the homes that meet the home filter requirements for the cities of interest
# 5. Make a datatable that attaches the school district rankings and commute score to the homes queried
## API to get cities from counties


# Functions

## General
def get_api_key(api_key_id = "Realtor"):
    """
    Gets the api key for website access.

    Table of key type and key value stored locally for privacy.

    :param api_key_id: key value in dataframe
    :return: api_key

    """

    # load api keys file
    df_api_keys = pd.read_csv("api_key_table.csv")

    # try to get api key
    try:
        api_key = df_api_keys.loc[df_api_keys['API']==api_key_id,'Key'][0]
        return api_key
    except IndexError:
        # get api key id list
        api_key_id_list = df_api_keys['Id'].unique().tolist()
        # print error message
        print('Cannot map key. Api key id must be one of the following options {0}'.format(api_key_id_list))


## Real Estate API
def get_listings(api_key,city,state_code,price_min, price_max, beds_min, baths_min, prop_type="single_family",limit=200):
    """

    :param city: str type
    :param state_code: str type (abbreviation ex: "NY")
    :param price_min: int
    :param price_max: int
    :param beds_min: int
    :param baths_min: int
    :param prop_type: str type Options - [single_family,multi_family,condo, mobile,land, farm,other]
    :param limit:  int
    :return: dataframe of real estate listings

    """


    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

    querystring = {
        "city": city,
        "state_code": state_code,
        "price_min": price_min,
        "price_max": price_max,
        "beds_min": beds_min,
        "baths_min": baths_min,
        "prop_type": prop_type,
        "limit": limit,
        "offset": "0",
        "sort": "relevance"
    }

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "realtor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response_json = response.json()

    # empty dataframe
    dataframe_list = []

    # iterate through each for sale listing
    for l in response_json['properties']:
        # convert each listing to dataframe
        _temp_df = pd.DataFrame.from_dict(l, orient='index').T

        # append to dataframe list for all listings
        dataframe_list.append(_temp_df)

    # concatenate all dataframes, for missing col values enter null value
    return pd.concat(dataframe_list, axis=0, ignore_index=True, sort=False)


def get_commute_score(r_api_key,w_api_key,lon,lat,address):
    url = "https://walk-score.p.rapidapi.com/score"

    querystring = {
        "lon": "undefined",
        "lat": "undefined",
        "address": "undefined",
        "wsapikey": "undefined"
    }

    headers = {
        'x-rapidapi-key': r_api_key,
        'x-rapidapi-host': "walk-score.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


test = get_listings(get_api_key("realtor"),"Fort Lee","NJ",200000,1000000,2,1)
test.to_csv("test.csv",index=False)

