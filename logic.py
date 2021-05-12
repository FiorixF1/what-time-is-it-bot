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



def generate_time_from_country(country, print_name=False):
    result = []
    for timezone, city in country.timezones:
        result.append(generate_time(country.code, country.emoji, country.name, timezone, city, print_name))
    return '\n'.join(result)

def generate_time(code, emoji, name, timezone, city, print_name=True):
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    return "{} {}{}: {}".format(emoji,
                                city,
                                f" ({name})" if print_name and name != "" and name != city else "",
                                now.strftime('%Y-%m-%d %H:%M:%S'))



def logic(query):
    response = []

    # garbage
    if len(query) < 2:
        return ''

    # query by country code
    country_code = query.upper()
    if country_code in dictionary:
        response.append(generate_time_from_country(dictionary[country_code]))
    else:
        # query by country name
        country_code = None
        
        for key in dictionary:
            # search a country by full name or alias
            if any(map(lambda string: fuzzy_equal(query, string), [dictionary[key].name] + dictionary[key].aliases)):
                country_code = key
                print_name = False
                break
        if country_code == None:
            # if you have not found a country, search by whole word only, so "man" matches with "Isle of Man" but not with "Germany"
            for key in dictionary:
                if any(map(lambda string: strict_search(query, string), [dictionary[key].name] + dictionary[key].aliases)):
                    country_code = key
                    print_name = True
                    break
        if country_code == None:
            # if you have not found a country, do a fuzzy research (this way "Ital" matches with "Italy")
            for key in dictionary:
                if any(map(lambda string: fuzzy_search(query, string), [dictionary[key].name] + dictionary[key].aliases)):
                    country_code = key
                    print_name = True
                    break
        
        if country_code != None:
            # query by country name
            response.append(generate_time_from_country(dictionary[country_code], print_name))
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
