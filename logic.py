import unidecode
import datetime
import pickle
import pytz
import json
import re



with open("countries.json", "r") as dump:
    countries = json.loads(dump.read())

with open("cities.json", "r") as dump:
    cities = json.loads(dump.read())



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
    for timezone, city in country["timezones"]:
        result.append(generate_time(country["code"], country["emoji"], country["name"], timezone, city, print_name))
    return '\n'.join(result)

def generate_time(code, emoji, name, timezone, city, print_name=True):
    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    return "{} {}{}: {}".format(emoji,
                                city,
                                f" ({name})" if print_name and name != "" and name != city else "",
                                now.strftime('%Y-%m-%d %H:%M:%S'))



def search_by_country_code(query):
    country_code = query.upper()
    if country_code in countries:
        return generate_time_from_country(countries[country_code])
    return ""

def search_by_country_full(query):    
    # search a country by full name or alias
    for key in countries:
        if any(map(lambda string: fuzzy_equal(query, string), [countries[key]["name"]] + countries[key]["aliases"])):
            return generate_time_from_country(countries[key], False)
    return ""
   
def search_by_city_tz(query):
    for key in countries:
        country = countries[key]
        for timezone, city in country["timezones"]:
            if fuzzy_search(query, city):
                return generate_time(country["code"], country["emoji"], country["name"], timezone, city)
    return ""

def search_by_city_db(query):
    result = []
    city_key = unidecode.unidecode(query.lower())
    if city_key in cities:
        for city in cities[city_key]:
            short_code  = city["country"]
            long_code   = short_code + "-" + city["region"]
            country     = countries[long_code] if long_code in countries else countries[short_code]
            result.append(generate_time(country["code"], country["emoji"], country["name"], city["timezone"], city["name"]))
    return "\n".join(result)

def search_by_country_subword(query):    
    # if you have not found a country, search by whole word only, so "man" matches with "Isle of Man" but not with "Germany"
    for key in countries:
        if any(map(lambda string: strict_search(query, string), [countries[key]["name"]] + countries[key]["aliases"])):
            return generate_time_from_country(countries[key], True)
    return ""

def search_by_country_substring(query):    
    # if you have not found a country, do a fuzzy research (this way "Ital" matches with "Italy")
    for key in countries:
        if any(map(lambda string: fuzzy_search(query, string), [countries[key]["name"]] + countries[key]["aliases"])):
            return generate_time_from_country(countries[key], True)
    return ""

def search_by_city_subword(query):
    result = []
    for city_key in cities:
        if strict_search(query, city_key):
            for city in cities[city_key]:
                short_code  = city["country"]
                long_code   = short_code + "-" + city["region"]
                country     = countries[long_code] if long_code in countries else countries[short_code]
                result.append(generate_time(country["code"], country["emoji"], country["name"], city["timezone"], city["name"]))
    return "\n".join(result)

def search_by_city_substring(query):
    result = []
    for city_key in cities:
        if fuzzy_search(query, city_key):
            for city in cities[city_key]:
                short_code  = city["country"]
                long_code   = short_code + "-" + city["region"]
                country     = countries[long_code] if long_code in countries else countries[short_code]
                result.append(generate_time(country["code"], country["emoji"], country["name"], city["timezone"], city["name"]))
    return "\n".join(result)



def logic(query):
    # garbage
    if len(query) < 2:
        return ""

    # PRIORITY:
    # - Country code
    # - Country name (full)
    # - City name (from timezone)
    # - City name (from database)
    # - Country name (subword)
    # - Country name (substring)
    # - City name (subword)
    # - City name (substring)

    researchers = [
        search_by_country_code,
        search_by_country_full,
        search_by_city_db,
        search_by_country_subword,
        search_by_country_substring,
        search_by_city_tz,
        search_by_city_subword,
        search_by_city_substring
    ]
    
    for research in researchers:
        response = research(query)
        if response:
            return response

    return ""
