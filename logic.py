import datetime
import pytz
import re

from flags import flags

# in order to avoid spam, many timezones are removed (also because they make no sense)
# why 12 timezones for Argentina and even 6 for Alaska?
removed_timezones = {
    "America/Adak",
    "America/Araguaina",
    "America/Argentina/Catamarca",
    "America/Argentina/Cordoba",
    "America/Argentina/Jujuy",
    "America/Argentina/La_Rioja",
    "America/Argentina/Mendoza",
    "America/Argentina/Rio_Gallegos",
    "America/Argentina/Salta",
    "America/Argentina/San_Juan",
    "America/Argentina/San_Luis",
    "America/Argentina/Tucuman",
    "America/Argentina/Ushuaia",
    "America/Atikokan",
    "America/Bahia",
    "America/Bahia_Banderas",
    "America/Blanc-Sablon",
    "America/Boa_Vista",
    "America/Boise",
    "America/Cambridge_Bay",
    "America/Campo_Grande",
    "America/Cancun",
    "America/Creston",
    "America/Cuiaba",
    "America/Dawson",
    "America/Dawson_Creek",
    "America/Eirunepe",
    "America/Fort_Nelson",
    "America/Glace_Bay",
    "America/Goose_Bay",
    "America/Hermosillo",
    "America/Indiana/Knox",
    "America/Indiana/Marengo",
    "America/Indiana/Petersburg",
    "America/Indiana/Tell_City",
    "America/Indiana/Vevay",
    "America/Indiana/Vincennes",
    "America/Indiana/Winamac",
    "America/Inuvik",
    "America/Iqaluit",
    "America/Juneau",
    "America/Kentucky/Louisville",
    "America/Kentucky/Monticello",
    "America/Maceio",
    "America/Matamoros",
    "America/Mazatlan",
    "America/Menominee",
    "America/Merida",
    "America/Metlakatla",
    "America/Moncton",
    "America/Monterrey",
    "America/Nipigon",
    "America/Nome",
    "America/Noronha",
    "America/North_Dakota/Beulah",
    "America/North_Dakota/Center",
    "America/North_Dakota/New_Salem",
    "America/Ojinaga",
    "America/Pangnirtung",
    "America/Porto_Velho",
    "America/Rainy_River",
    "America/Rankin_Inlet",
    "America/Resolute",
    "America/Rio_Branco",
    "America/Santarem",
    "America/Sitka",
    "America/St_Johns",
    "America/Swift_Current",
    "America/Thunder_Bay",
    "America/Whitehorse",
    "America/Yakutat",
    "America/Yellowknife",
    "Asia/Chita",
    "Asia/Urumqi",
    "Australia/Broken_Hill",
    "Australia/Currie",
    "Australia/Eucla",
    "Australia/Hobart",
    "Australia/Lindeman",
    "Australia/Lord_Howe",
    "Europe/Astrakhan",
    "Europe/Kirov"
}



def get_time_from_region(code, region):
    emoji = "🏳️"
    for flag in flags:
        # use country code when available, otherwise fallback to region name
        # matching is done with whole words only, so "man" matches with "Isle of Man" but not with "Germany"
        if code and flag["code"] == code or not code and re.search(rf'\b{flag["name"]}\b', region.replace('_', ' '), re.IGNORECASE):
            emoji = flag["emoji"]
            break

    if emoji == "🏳️" and not code:
        for flag in flags:
            # if you have not found a country, do a fuzzy research (this way "Ital" matches with "Italy")
            if flag["name"].lower() in region.lower():
                emoji = flag["emoji"]
                break

    if '/' in region:
        city = region[region.rfind('/')+1:].replace('_', ' ')
    else:
        city = region.replace('_', ' ')

    tz = pytz.timezone(region)
    now = datetime.datetime.now(tz)
    return "{} {}: {}".format(emoji, city, now.strftime('%Y-%m-%d %H:%M:%S'))



def logic(query):
    response = []

    # preprocessing
    query = "US" if query.lower() == "usa"               else query
    query = "GB" if query.lower() == "uk"                else query
    query = "GB" if query.lower() == "england"           else query
    query = "GB" if query.lower() == "scotland"          else query
    query = "GB" if query.lower() == "wales"             else query
    query = "GB" if query.lower() == "northern ireland"  else query
    query = "KP" if query.lower() == "north korea"       else query
    query = "KR" if query.lower() == "south korea"       else query
    query = "WS" if query.lower() == "samoa"             else query
    query = "AS" if query.lower() == "american samoa"    else query
    query = "CG" if query.lower() == "congo"             else query
    query = "CD" if query.lower() == "democratic congo"  else query
    query = "GN" if query.lower() == "guinea"            else query
    query = "GQ" if query.lower() == "equatorial guinea" else query
    query = "SD" if query.lower() == "sudan"             else query
    query = "SS" if query.lower() == "south sudan"       else query
    
    
    
    
    
    
    # garbage
    if len(query) < 2:
        return ''

    if len(query) == 2:
        # query by country code
        country_code = query.upper()
        timezones = set(pytz.country_timezones.get(country_code, [])) - removed_timezones

        for region in timezones:
            response.append(get_time_from_region(country_code, region))
    elif query.lower() == "utc":
        # handle UTC separately
        response.append(get_time_from_region('', "UTC").replace("🏳️", "🌍"))
    
    # search by country or city name (also for queries with two letters)
    if response == []:
        country_code = None
        for key in pytz.country_names:
            # matching is done with whole words only, so "man" matches with "Isle of Man" but not with "Germany"
            if re.search(rf"\b{query}\b", pytz.country_names[key], re.IGNORECASE):
                country_code = key
                break
        
        if country_code == None:
            # if you have not found a country, do a fuzzy research (this way "Ital" matches with "Italy")
            for key in pytz.country_names:
                if query.lower() in pytz.country_names[key].lower():
                    country_code = key
                    break

        if country_code != None:
            # query by country name
            timezones = set(pytz.country_timezones.get(country_code, [])) - removed_timezones

            for region in timezones:
                response.append(get_time_from_region(country_code, region))
        else:
            # query by city name
            for country_code in pytz.country_names:
                for region in set(pytz.country_timezones.get(country_code, [])) - removed_timezones:
                    if query.lower().replace(' ', '_') in region.lower():
                        response.append(get_time_from_region(country_code, region))
            if len(response) == 0:
                # other queries
                for region in pytz.common_timezones:
                    if query.lower().replace(' ', '_') in region.lower():
                        response.append(get_time_from_region('', region))

    return '\n'.join(response)

