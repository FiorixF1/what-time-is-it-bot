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
add_alias("KP", "DPRK")
add_alias("KP", "North Corea")
add_alias("KR", "Corea")
add_alias("KR", "Korea")
add_alias("KR", "South Corea")
add_alias("MC", "Montecarlo")
add_alias("ME", "Montenigga")
add_alias("MM", "Burma")
add_alias("MO", "Macau")
add_alias("NF", "Norfolk")
add_alias("NL", "Holland")
add_alias("NZ", "Kiwi")
add_alias("SZ", "Eswatini")
add_alias("TL", "Timor East")
add_alias("TL", "Timor Est")
add_alias("US", "USA")
add_alias("VA", "Vatican")



# Step 4: add countries and regions (code is ISO 3166-2 from Wikipedia)
countries["BV"]     = create_country("BV",     "🇧🇻", "Bouvet Island",   list(), [("Europe/Oslo", "Bouvet")])

countries["RS-VO"]  = create_country("RS-VO",  "🇷🇸", "Vojvodina",       list(), [("Europe/Belgrade", "Novi Sad")])
countries["XK"]     = create_country("XK",     "🇽🇰", "Kosovo",          list(), [("Europe/Belgrade", "Pristina")])

countries["GB-ENG"] = create_country("GB-ENG", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "England",         list(), [("Europe/London", "London")])
countries["GB-SCT"] = create_country("GB-SCT", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Scotland",        list(), [("Europe/London", "Edimburgh")])
countries["GB-WLS"] = create_country("GB-WLS", "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Wales",           list(), [("Europe/London", "Cardiff")])
countries["GB-NIR"] = create_country("GB-NIR", "🇬🇧", "Northern Ireland",list(), [("Europe/London", "Belfast")])

countries["FM-TRK"] = create_country("FM-TRK", "🇫🇲", "Chuuk",           list(), [("Pacific/Chuuk", "Chuuk")])
countries["FM-KSA"] = create_country("FM-KSA", "🇫🇲", "Kosrae",          list(), [("Pacific/Kosrae", "Kosrae")])
countries["FM-PNI"] = create_country("FM-PNI", "🇫🇲", "Pohnpei",         list(), [("Pacific/Pohnpei", "Pohnpei")])
countries["FM-YAP"] = create_country("FM-YAP", "🇫🇲", "Yap",             list(), [("Pacific/Chuuk", "Yap")])

countries["RU-CE"]  = create_country("RU-CE",  "🇷🇺󠁧󠁢󠁷󠁬󠁳󠁿", "Chechnya",        list(), [("Europe/Moscow", "Grozny")])

countries["IT-25"]  = create_country("IT-25",  "🇮🇹", "Padania",         list(), [("Europe/Rome", "Milan")])
countries["IT-72"]  = create_country("IT-72",  "🇮🇹", "Terronia",        list(), [("Europe/Rome", "Naples")])

countries["UA-11"]  = create_country("UA-11",  "🇺🇦", "Crimea",          list(), [("Europe/Simferopol", "Simferopol")])

countries["ID-BA"]  = create_country("ID-BA",  "🇮🇩", "Bali",            list(), [("Asia/Makassar", "Denpasar")])
countries["ID-JW"]  = create_country("ID-JW",  "🇮🇩", "Java",            list(), [("Asia/Jakarta", "Jakarta")])
countries["ID-KA"]  = create_country("ID-KA",  "🇮🇩", "Borneo",          list(), [("Asia/Pontianak", "Pontianak")])
countries["ID-PP"]  = create_country("ID-PP",  "🇮🇩", "West Papua",      list(), [("Asia/Jayapura", "Jayapura")])
countries["ID-SL"]  = create_country("ID-SL",  "🇮🇩", "Sulawesi",        list(), [("Asia/Makassar", "Makassar")])
countries["ID-SM"]  = create_country("ID-SM",  "🇮🇩", "Sumatra",         list(), [("Asia/Jakarta", "Medan")])

countries["US-AK"]  = create_country("US-AK",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Alaska",          list(), [("America/Anchorage", "Anchorage"), ("America/Adak", "Adak")])
countries["US-AZ"]  = create_country("US-AZ",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Arizona",         list(), [("America/Phoenix", "Phoenix"), ("America/Shiprock", "Tuba City")])
countries["US-AZx"] = create_country("US-AZx", "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Navajo Nation",   list(), [("America/Shiprock", "Window Rock")])
countries["US-CA"]  = create_country("US-CA",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "California",      list(), [("America/Los_Angeles", "Los Angeles")])
countries["US-FL"]  = create_country("US-FL",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Florida",         list(), [("America/New_York", "Miami"), ("America/Chicago", "Pensacola")])
countries["US-HI"]  = create_country("US-HI",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Hawaii",          list(), [("Pacific/Honolulu", "Honolulu")])
countries["US-NV"]  = create_country("US-NV",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Nevada",          list(), [("America/Los_Angeles", "Las Vegas")])
countries["US-NY"]  = create_country("US-NY",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "New York",        list(), [("America/New_York", "New York City")])
countries["US-TX"]  = create_country("US-TX",  "🇺🇸󠁧󠁢󠁷󠁬󠁳󠁿", "Texas",           list(), [("America/Chicago", "Dallas")])

countries["CN-XJ"]  = create_country("CN-XJ",  "🇨🇳󠁧󠁢󠁷󠁬󠁳󠁿", "Xinjiang",        list(), [("Asia/Urumqi", "Ürümqi")])
countries["CN-XZ"]  = create_country("CN-XZ",  "🇨🇳󠁧󠁢󠁷󠁬󠁳󠁿", "Tibet",           list(), [("Asia/Shanghai", "Lhasa")])

# not official code
countries["LL"]     = create_country("LL",     "🏳️", "Liberland",       list(), [("Europe/Prague", "Liberland")])

# not official code
# Timor East time (UTC+9:00 without DST)
# Italian time (UTC+1:00 with DST)
# Nauruan time (UTC+12:00 without DST)
countries["RX"]     = create_country("RX",     "🏳️", "RadioSex",        list(), [("Asia/Dili", "Motore"), ("Asia/Dili", "Arese"), ("Asia/Dili", "Rock Raider"), ("Europe/Rome", "Mici e Micetti QUEST"), ("Pacific/Nauru", "Nauru")])

countries["UTC"]    = create_country("UTC",    "🌍", "World",           ["Earth", "Gea", "Terra"], [("UTC", "UTC")])



# Step 5: add a placeholder for the remaining timezones of the library
missing_timezones = pytz.common_timezones_set - REMOVED_TIMEZONES
for country in countries:
    for timezone, _ in countries[country]["timezones"]:
        missing_timezones -= {timezone}
countries[""] = create_country("", "🏳️", "", list(), list(map(lambda x: (x, get_city_from_timezone(x)), missing_timezones)))



# Step 6: store on disk
with open("countries.json", "w", encoding='utf8') as dump:
    dump.write(json.dumps(countries, indent=2))



# Step 7: debug
for elem in countries:
    print(countries[elem])



### REGIONS

# Step 1: get available data from "admin1CodesASCII.txt"
regions = dict()

with open("admin1CodesASCII.txt", "r", encoding='utf8') as dump:
    while True:
        line = dump.readline()
        if line == "":
            break
        
        region_record = line.split("\t")
        
        code          = region_record[0].replace(".", "-")
        name          = region_record[1]

        regions[code] = name



# Step 2: store on disk
with open("regions.json", "w", encoding='utf8') as dump:
    dump.write(json.dumps(regions, indent=2))



### CITIES

def create_city(name, country, region, timezone):
    return {
        "name"     : name,
        "country"  : country,
        "region"   : region,
        "timezone" : timezone
    }

def add_city(name, country, region, timezone):
    purified_name = unidecode.unidecode(name.lower())
    
    if purified_name not in cities:
        cities[purified_name] = [create_city(name, country, region, timezone)]
    else:
        cities[purified_name].append(create_city(name, country, region, timezone))


        
# Step 1: get available data from "cities15000.txt"
cities = dict()

with open("cities15000.txt", "r", encoding='utf8') as dump:
    while True:
        line = dump.readline()
        if line == "":
            break
        
        city_record = line.split("\t")
        
        name          = city_record[1]
        country       = city_record[8]
        region        = city_record[10]
        timezone      = city_record[17]

        add_city(name, country, region, timezone)



# Step 2: add custom cities and aliases
add_city("Area 51",              "US", "NV", "America/Los_Angeles")
add_city("Liberty City",         "US", "NY", "America/New_York")
add_city("Vice City",            "US", "FL", "America/New_York")
add_city("Los Santos",           "US", "CA", "America/Los_Angeles")
add_city("San Fierro",           "US", "CA", "America/Los_Angeles")
add_city("Las Venturas",         "US", "NV", "America/Los_Angeles")

add_city("Chornobyl\u2019",      "UA", "13", "Europe/Kiev")  # real spelling
add_city("Chernobyl\u2019",      "UA", "13", "Europe/Kiev")  # common spelling
add_city("Pripyat",              "UA", "13", "Europe/Kiev")

add_city("Königsberg",           "RU", "23", "Europe/Kaliningrad")

add_city("Nagyvárad",            "RO", "05", "Europe/Bucharest")
add_city("Temesvár",             "RO", "36", "Europe/Bucharest")
add_city("Kolozsvár",            "RO", "13", "Europe/Bucharest")
add_city("Brassó",               "RO", "09", "Europe/Bucharest")
add_city("Marosvásárhely",       "RO", "27", "Europe/Bucharest")
add_city("Sepsiszentgyörgy",     "RO", "15", "Europe/Bucharest")
add_city("Csíkszereda",          "RO", "20", "Europe/Bucharest")
add_city("Székelyudvarhely",     "RO", "20", "Europe/Bucharest")
add_city("Kézdivásárhely",       "RO", "15", "Europe/Bucharest")

add_city("Ungvár",               "UK", "25", "Europe/Kyiv")
add_city("Beregszász",           "UK", "25", "Europe/Kyiv")
add_city("Munkács",              "UK", "25", "Europe/Kyiv")
add_city("Huszt",                "UK", "25", "Europe/Kyiv")

add_city("Bozen",                "IT", "17", "Europe/Rome")
add_city("Capodistria",          "SI", "50", "Europe/Ljubljana")
add_city("Fiume",                "HR", "12", "Europe/Zagreb")

add_city("Motore",               "RX", "01", "Asia/Dili")
add_city("Arese",                "RX", "02", "Asia/Dili")
add_city("Rock Raider",          "RX", "03", "Asia/Dili")
add_city("Mici e Micetti QUEST", "RX", "04", "Europe/Rome")



# Step 3: store on disk
with open("cities.json", "w", encoding='utf8') as dump:
    dump.write(json.dumps(cities, indent=2))
