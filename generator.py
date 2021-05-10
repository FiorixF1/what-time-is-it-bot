from collections import namedtuple
from flags import flags
import unidecode
import pickle
import pytz

def get_city_from_timezone(timezone):
    if '/' in timezone:
        return timezone[timezone.rfind('/')+1:].replace('_', ' ')
    else:
        return timezone.replace('_', ' ')



Country = namedtuple("Country", ["code", "emoji", "name", "timezones"])

dictionary = dict()



# Step 1: get available data from "flags" and "pytz"
for flag in flags:
    code      = flag["code"]
    emoji     = flag["emoji"]
    name      = flag["name"]
    timezones = pytz.country_timezones.get(code, [])
    cities    = map(get_city_from_timezone, timezones)
    timezones_and_cities = list(zip(timezones, cities))
    
    dictionary[code] = Country(code, emoji, name, timezones_and_cities)



# Step 2: remove useless timezones
REMOVED_TIMEZONES = {
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
    "Canada/Atlantic",
    "Canada/Central",
    "Canada/Eastern",
    "Canada/Mountain",
    "Canada/Newfoundland",
    "Canada/Pacific",
    "Europe/Astrakhan",
    "Europe/Busingen",
    "Europe/Kirov",
    "US/Alaska",
    "US/Arizona",
    "US/Central",
    "US/Eastern",
    "US/Hawaii",
    "US/Mountain",
    "US/Pacific",
}

for country in dictionary:
    old = dictionary[country]
    new = Country(old.code, old.emoji, old.name, list(filter(lambda timezone: timezone[0] not in REMOVED_TIMEZONES, old.timezones)))
    dictionary[country] = new



# Step 3: add custom entries
dictionary["XK"]    = Country("XK",    "🇽🇰", "Kosovo",   [("Europe/Tirane", "Pristina")])
dictionary["ENG"]   = Country("ENG",   "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "England",  [("Europe/London", "London")])
dictionary["SCT"]   = Country("SCT",   "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Scotland", [("Europe/London", "Edimburgh")])
dictionary["WLS"]   = Country("WLS",   "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Wales",    [("Europe/London", "Cardiff")])
dictionary["RU-CE"] = Country("RU-CE", "🇷🇺󠁧󠁢󠁷󠁬󠁳󠁿", "Chechnya", [("Europe/Moscow", "Grozny")])
dictionary["KGD"]   = Country("KGD",   "🇷🇺󠁧󠁢󠁷󠁬󠁳󠁿", "Russia",   [("Europe/Kaliningrad", "Königsberg")])
dictionary["UA-43"] = Country("UA-43", "🇺🇦", "Crimea",   [("Europe/Simferopol", "Simferopol")])
dictionary["US-AK"] = Country("US-AK", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Alaska",   [("US/Alaska", "Anchorage")])
dictionary["US-HI"] = Country("US-HI", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Hawaii",   [("US/Hawaii", "Honolulu")])
dictionary["US-FL"] = Country("US-FL", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Florida",  [("America/New_York", "Miami")])
dictionary["CN-BJ"] = Country("CN-BJ", "🇨🇳󠁧󠁢󠁷󠁬󠁳󠁿", "China",    [("Asia/Shanghai", "Beijing")])
dictionary["IN-DL"] = Country("IN-DL", "🇮🇳", "India",    [("Asia/Kolkata", "New Delhi")])
dictionary["UTC"]   = Country("UTC",   "🌍", "World",    [("UTC", "UTC")])



# Step 4: add a placeholder for the remaining timezones of the library
missing_timezones = pytz.common_timezones_set - REMOVED_TIMEZONES
for country in dictionary:
    for timezone, _ in dictionary[country].timezones:
        missing_timezones -= {timezone}
dictionary[""] = Country("", "🏳️", "", list(map(lambda x: (x, get_city_from_timezone(x)), missing_timezones)))



# Step 5: store on disk
#pickle.dump(dictionary, open("db.p", "wb"))



# Step 6: debug
for elem in dictionary:
    print(dictionary[elem])

