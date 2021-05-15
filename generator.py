from flags import flags
import unidecode
import pickle
import pytz
import json



### COUNTRIES

def create_country(code, emoji, name, aliases, timezones):
    return {
        "code"      : code,
        "emoji"     : emoji,
        "name"      : name,
        "aliases"   : aliases,
        "timezones" : timezones
    }

def add_alias(code, alias):
    countries[code]["aliases"] = countries[code]["aliases"] + [alias]

def get_city_from_timezone(timezone):
    if '/' in timezone:
        return timezone[timezone.rfind('/')+1:].replace('_', ' ')
    else:
        return timezone.replace('_', ' ')



# Step 1: get available data from "flags" and "pytz"
countries = dict()

for flag in flags:
    code      = flag["code"]
    emoji     = flag["emoji"]
    name      = flag["name"]
    aliases   = list()
    timezones = pytz.country_timezones.get(code, [])
    cities    = map(get_city_from_timezone, timezones)
    timezones_and_cities = list(zip(timezones, cities))

    countries[code] = create_country(code, emoji, name, aliases, timezones_and_cities)



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

for code in countries:
    countries[code]["timezones"] = list(filter(lambda timezone: timezone[0] not in REMOVED_TIMEZONES, countries[code]["timezones"]))



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
add_alias("NZ", "Kiwi")
add_alias("SZ", "Eswatini")
add_alias("TL", "Timor East")
add_alias("TL", "Timor Est")
add_alias("US", "USA")
add_alias("VA", "Vatican")



# Step 4: add countries and regions
countries["BV"]     = create_country("BV",     "🇧🇻", "Bouvet Island",   list(), [("Europe/Oslo", "Bouvet")])

countries["XK"]     = create_country("XK",     "🇽🇰", "Kosovo",          list(), [("Europe/Belgrade", "Pristina")])

countries["GB-ENG"] = create_country("GB-ENG", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "England",         list(), [("Europe/London", "London")])
countries["GB-SCT"] = create_country("GB-SCT", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Scotland",        list(), [("Europe/London", "Edimburgh")])
countries["GB-WLS"] = create_country("GB-WLS", "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Wales",           list(), [("Europe/London", "Cardiff")])

countries["FM-TRK"] = create_country("FM-TRK",    "🇫🇲", "Chuuk",           list(), [("Pacific/Chuuk", "Chuuk")])
countries["FM-KSA"] = create_country("FM-KSA",    "🇫🇲", "Kosrae",          list(), [("Pacific/Kosrae", "Kosrae")])
countries["FM-PNI"] = create_country("FM-PNI",    "🇫🇲", "Pohnpei",         list(), [("Pacific/Pohnpei", "Pohnpei")])
countries["FM-YAP"] = create_country("FM-YAP",    "🇫🇲", "Yap",             list(), [("Pacific/Chuuk", "Yap")])

countries["RU-CE"]  = create_country("RU-CE",  "🇷🇺󠁧󠁢󠁷󠁬󠁳󠁿", "Chechnya",        list(), [("Europe/Moscow", "Grozny")])
countries["KGD"]    = create_country("KGD",    "🇷🇺󠁧󠁢󠁷󠁬󠁳󠁿", "Russia",          list(), [("Europe/Kaliningrad", "Königsberg")])

countries["UA-43"]  = create_country("UA-43",  "🇺🇦", "Crimea",          list(), [("Europe/Simferopol", "Simferopol")])

countries["ID-JW"]  = create_country("ID-JW",  "🇮🇩", "Java",            list(), [("Asia/Jakarta", "Jakarta")])
countries["ID-KA"]  = create_country("ID-KA",  "🇮🇩", "Borneo",          list(), [("Asia/Pontianak", "Pontianak")])
countries["ID-NU"]  = create_country("ID-NU",  "🇮🇩", "Nusa Tenggara",   list(), [("Asia/Makassar", "Bali")])
countries["ID-PP"]  = create_country("ID-PP",  "🇮🇩", "West Papua",      list(), [("Asia/Jayapura", "Jayapura")])
countries["ID-SL"]  = create_country("ID-SL",  "🇮🇩", "Sulawesi",        list(), [("Asia/Makassar", "Makassar")])
countries["ID-SM"]  = create_country("ID-SM",  "🇮🇩", "Sumatra",         list(), [("Asia/Jakarta", "Medan")])

countries["US-AK"]  = create_country("US-AK",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Alaska",          list(), [("US/Alaska", "Anchorage"), ("America/Adak", "Adak")])
countries["US-CA"]  = create_country("US-CA",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "California",      list(), [("US/Pacific", "Los Angeles")])
countries["US-HI"]  = create_country("US-HI",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Hawaii",          list(), [("US/Hawaii", "Honolulu")])
countries["US-FL"]  = create_country("US-FL",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Florida",         list(), [("US/Eastern", "Miami"), ("US/Central", "Pensacola")])
countries["US-TX"]  = create_country("US-TX",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Texas",           list(), [("US/Central", "Dallas")])

countries["CN-XJ"]  = create_country("CN-XJ",  "🇨🇳󠁧󠁢󠁷󠁬󠁳󠁿", "Xinjiang",        list(), [("Asia/Urumqi", "Ürümqi")])
countries["CN-XZ"]  = create_country("CN-XZ",  "🇨🇳󠁧󠁢󠁷󠁬󠁳󠁿", "Tibet",           list(), [("Asia/Shanghai", "Lhasa")])

countries["UTC"]    = create_country("UTC",    "🌍", "World",           ["Earth", "Gea", "Terra"], [("UTC", "UTC")])



# Step 5: add a placeholder for the remaining timezones of the library
missing_timezones = pytz.common_timezones_set - REMOVED_TIMEZONES
for country in countries:
    for timezone, _ in countries[country]["timezones"]:
        missing_timezones -= {timezone}
countries[""] = create_country("", "🏳️", "", list(), list(map(lambda x: (x, get_city_from_timezone(x)), missing_timezones)))



# Step 6: store on disk
with open("countries.json", "w") as dump:
    dump.write(json.dumps(countries, indent=2))



# Step 7: debug
for elem in countries:
    print(countries[elem])



### CITIES

def create_city(name, country, region, timezone):
    return {
        "name"     : name,
        "country"  : country,
        "region"   : region,
        "timezone" : timezone
    }



# Step 1: get available data from "cities15000.txt"
cities = dict()

with open("cities15000.txt", "r") as dump:
    while True:
        line = dump.readline()
        if line == "":
            break
        
        city_record = line.split("\t")
        
        purified_name = unidecode.unidecode(city_record[1].lower())
        name          = city_record[1]
        country       = city_record[8]
        region        = city_record[10]
        timezone      = city_record[17]

        if purified_name not in cities:
            cities[purified_name] = [create_city(name, country, region, timezone)]
        else:
            cities[purified_name].append(create_city(name, country, region, timezone))



# Step 2: store on disk
with open("cities.json", "w") as dump:
    dump.write(json.dumps(cities, indent=2))