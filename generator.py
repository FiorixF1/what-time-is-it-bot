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

def add_alias(code, alias):
    old = dictionary[code]
    new = Country(old.code,
                  old.emoji,
                  old.name,
                  old.aliases + [alias],
                  old.timezones)
    dictionary[code] = new



Country = namedtuple("Country", ["code", "emoji", "name", "aliases", "timezones"])

dictionary = dict()



# Step 1: get available data from "flags" and "pytz"
for flag in flags:
    code      = flag["code"]
    emoji     = flag["emoji"]
    name      = flag["name"]
    aliases   = list()
    timezones = pytz.country_timezones.get(code, [])
    cities    = map(get_city_from_timezone, timezones)
    timezones_and_cities = list(zip(timezones, cities))
    
    dictionary[code] = Country(code, emoji, name, aliases, timezones_and_cities)



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
    "America/North_Dakota/Beulah",
    "America/North_Dakota/Center",
    "America/North_Dakota/New_Salem",
    "America/Ojinaga",
    "America/Pangnirtung",
    "America/Porto_Velho",
    "America/Rainy_River",
    "America/Rankin_Inlet",
    "America/Resolute",
    "America/Santarem",
    "America/Sitka",
    "America/Swift_Current",
    "America/Thunder_Bay",
    "America/Whitehorse",
    "America/Yakutat",
    "America/Yellowknife",
    "Asia/Chita",
    "Asia/Urumqi",
    "Australia/Broken_Hill",
    "Australia/Currie",
    "Australia/Hobart",
    "Australia/Lindeman",
    "Canada/Atlantic",
    "Canada/Central",
    "Canada/Eastern",
    "Canada/Mountain",
    "Canada/Newfoundland",
    "Canada/Pacific",
    "Europe/Astrakhan",
    "Europe/Busingen",
    "Europe/Kirov",
    "Europe/Simferopol",
    "Europe/Uzhgorod",
    "Europe/Zaporozhye",
    "US/Alaska",
    "US/Arizona",
    "US/Central",
    "US/Eastern",
    "US/Hawaii",
    "US/Mountain",
    "US/Pacific"
}

for code in dictionary:
    old = dictionary[code]
    new = Country(old.code,
                  old.emoji,
                  old.name,
                  old.aliases,
                  list(filter(lambda timezone: timezone[0] not in REMOVED_TIMEZONES, old.timezones
    )))
    dictionary[code] = new



# Step 3: add aliases for existing countries
add_alias("AE", "UAE")
add_alias("CD", "Big Congo")
add_alias("CG", "Small Congo")
add_alias("CI", "Ivory Coast")
add_alias("CM", "Camerun")
add_alias("GB", "Great Britain")
add_alias("GB", "UK")
add_alias("KP", "North Corea")
add_alias("KR", "Corea")
add_alias("KR", "Korea")
add_alias("KR", "South Corea")
add_alias("MC", "Montecarlo")
add_alias("ME", "Montenigga")
add_alias("MM", "Burma")
add_alias("MO", "Macau")
add_alias("NL", "Holland")
add_alias("SZ", "Eswatini")
add_alias("TL", "Timor East")
add_alias("TL", "Timor Est")
add_alias("US", "USA")
add_alias("VA", "Vatican")



# Step 4: add countries and cities
dictionary["BV"]    = Country("BV",    "🇧🇻", "Bouvet Island",   list(), [("Europe/Oslo", "Bouvet")])

dictionary["XK"]    = Country("XK",    "🇽🇰", "Kosovo",          list(), [("Europe/Tirane", "Pristina")])

dictionary["ENG"]   = Country("ENG",   "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "England",         list(), [("Europe/London", "London")])
dictionary["SCT"]   = Country("SCT",   "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Scotland",        list(), [("Europe/London", "Edimburgh")])
dictionary["WLS"]   = Country("WLS",   "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Wales",           list(), [("Europe/London", "Cardiff")])

dictionary["TRK"]   = Country("TRK",   "🇫🇲", "Chuuk",           list(), [("Pacific/Chuuk", "Chuuk")])
dictionary["KSA"]   = Country("KSA",   "🇫🇲", "Kosrae",          list(), [("Pacific/Kosrae", "Kosrae")])
dictionary["PNI"]   = Country("PNI",   "🇫🇲", "Pohnpei",         list(), [("Pacific/Pohnpei", "Pohnpei")])
dictionary["YAP"]   = Country("YAP",   "🇫🇲", "Yap",             list(), [("Pacific/Chuuk", "Yap")])

dictionary["RU-CE"] = Country("RU-CE", "🇷🇺󠁧󠁢󠁷󠁬󠁳󠁿", "Chechnya",        list(), [("Europe/Moscow", "Grozny")])
dictionary["KGD"]   = Country("KGD",   "🇷🇺󠁧󠁢󠁷󠁬󠁳󠁿", "Russia",          list(), [("Europe/Kaliningrad", "Königsberg")])

dictionary["UA-43"] = Country("UA-43", "🇺🇦", "Crimea",          list(), [("Europe/Simferopol", "Simferopol")])
dictionary["UA-14"] = Country("UA-14", "🇺🇦", "Donetsk",         list(), [("Europe/Moscow", "Donetsk")])
dictionary["UA-09"] = Country("UA-09", "🇺🇦", "Luhansk",         list(), [("Europe/Moscow", "Luhansk")])

dictionary["ID-JW"] = Country("ID-JW", "🇮🇩", "Java",            list(), [("Asia/Jakarta", "Jakarta")])
dictionary["ID-KA"] = Country("ID-KA", "🇮🇩", "Borneo",          list(), [("Asia/Pontianak", "Pontianak")])
dictionary["ID-NU"] = Country("ID-NU", "🇮🇩", "Nusa Tenggara",   list(), [("Asia/Makassar", "Bali")])
dictionary["ID-PP"] = Country("ID-PP", "🇮🇩", "West Papua",      list(), [("Asia/Jayapura", "Jayapura")])
dictionary["ID-SL"] = Country("ID-SL", "🇮🇩", "Sulawesi",        list(), [("Asia/Makassar", "Makassar")])
dictionary["ID-SM"] = Country("ID-SM", "🇮🇩", "Sumatra",         list(), [("Asia/Jakarta", "Medan")])

dictionary["US-AK"] = Country("US-AK", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Alaska",          list(), [("US/Alaska", "Anchorage"), ("America/Adak", "Adak")])
dictionary["US-CA"] = Country("US-CA", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "California",      list(), [("US/Pacific", "Los Angeles")])
dictionary["US-HI"] = Country("US-HI", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Hawaii",          list(), [("US/Hawaii", "Honolulu")])
dictionary["US-FL"] = Country("US-FL", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Florida",         list(), [("US/Eastern", "Miami"), ("US/Central", "Pensacola")])
dictionary["US-TX"] = Country("US-TX", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Texas",           list(), [("US/Central", "Dallas")])

dictionary["CN-BJ"] = Country("CN-BJ", "🇨🇳󠁧󠁢󠁷󠁬󠁳󠁿", "China",           list(), [("Asia/Shanghai", "Beijing")])
dictionary["CN-XJ"] = Country("CN-XJ", "🇨🇳󠁧󠁢󠁷󠁬󠁳󠁿", "Xinjiang",        list(), [("Asia/Urumqi", "Ürümqi")])

dictionary["IN-DL"] = Country("IN-DL", "🇮🇳", "India",           list(), [("Asia/Kolkata", "New Delhi")])

dictionary["UTC"]   = Country("UTC",   "🌍", "World",           ["Earth", "Gea", "Terra"], [("UTC", "UTC")])



# Step 5: add a placeholder for the remaining timezones of the library
missing_timezones = pytz.common_timezones_set - REMOVED_TIMEZONES
for country in dictionary:
    for timezone, _ in dictionary[country].timezones:
        missing_timezones -= {timezone}
dictionary[""] = Country("", "🏳️", "", list(), list(map(lambda x: (x, get_city_from_timezone(x)), missing_timezones)))



# Step 6: store on disk
#pickle.dump(dictionary, open("db.p", "wb"))



# Step 7: debug
for elem in dictionary:
    print(dictionary[elem])

