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
    :return: API Key

    """

    # load api keys file
    df_api_keys = pd.read_csv()

## Real Estate API
def real_estate_api():
    import requests

    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

    querystring = {"city": "New York City", "limit": "200", "offset": "0", "state_code": "NY", "sort": "relevance"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "realtor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)