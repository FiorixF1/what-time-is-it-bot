from collections import namedtuple
import unidecode
import datetime
import pickle
import pytz
import re

#Country = namedtuple("Country", ["code", "emoji", "name", "timezones"])

#dictionary = pickle.load(open("db.p", "rb"))

from generator import dictionary

def strict_search(query, string):
    query = unidecode.unidecode(query)
    string = unidecode.unidecode(string)
    return re.search(rf"\b{query}\b", string, re.IGNORECASE)

def fuzzy_search(query, string):
    query = unidecode.unidecode(query.lower())
    string = unidecode.unidecode(string.lower())
    return query in string

def fuzzy_equal(query, string):
    query = unidecode.unidecode(query.lower())
    string = unidecode.unidecode(string.lower())
    return query == string



def generate_time_from_country(country):
    result = []
    for timezone, city in country.timezones:
        result.append(generate_time(country.code, country.emoji, country.name, timezone, city, False))
    return '\n'.join(result)

def generate_time(code, emoji, name, timezone, city, show_country=True):
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    return "{} {}{}: {}".format(emoji,
                                city,
                                f" ({name})" if show_country and name != "" and name != city else "",
                                now.strftime('%Y-%m-%d %H:%M:%S'))



def logic(query):
    response = []

    # preprocessing
    query = "US" if fuzzy_equal(query, "usa")               else query
    query = "GB" if fuzzy_equal(query, "uk")                else query
    query = "KR" if fuzzy_equal(query, "korea")             else query
    query = "KP" if fuzzy_equal(query, "north korea")       else query
    query = "KR" if fuzzy_equal(query, "south korea")       else query
    query = "KR" if fuzzy_equal(query, "corea")             else query
    query = "KP" if fuzzy_equal(query, "north corea")       else query
    query = "KR" if fuzzy_equal(query, "south corea")       else query
    query = "WS" if fuzzy_equal(query, "samoa")             else query
    query = "AS" if fuzzy_equal(query, "american samoa")    else query
    query = "CG" if fuzzy_equal(query, "congo")             else query
    query = "CD" if fuzzy_equal(query, "democratic congo")  else query
    query = "MM" if fuzzy_equal(query, "burma")             else query

    # garbage
    if len(query) < 2:
        return ''

    # query by country code
    country_code = query.upper()
    if country_code in dictionary:
        response.append(generate_time_from_country(dictionary[country_code]))
    else:
        country_code = None
        # query by country name
        for key in dictionary:
            # matching is done with whole words only, so "man" matches with "Isle of Man" but not with "Germany"
            if strict_search(query, dictionary[key].name):
                country_code = key
                break
        if country_code == None:
            # if you have not found a country, do a fuzzy research (this way "Ital" matches with "Italy")
            for key in dictionary:
                if fuzzy_search(query, dictionary[key].name):
                    country_code = key
                    break
        
        if country_code != None:
            # query by country name
            response.append(generate_time_from_country(dictionary[country_code]))
        else:
            # query by city name
            for country_code in dictionary:
                if len(response) != 0:
                    break
                country = dictionary[country_code]
                for timezone, city in country.timezones:
                    if fuzzy_search(query, city):
                        response.append(generate_time(country.code, country.emoji, country.name, timezone, city))

    return '\n'.join(response)

