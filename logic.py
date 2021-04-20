import datetime
import pytz

from timezones import timezones
from flags import flags



def logic(query):
    response = []
    for timezone in timezones:
        country_code, region = timezone
        
        if query.upper() == country_code or len(query) > 2 and query.lower().replace(' ', '_') in region.lower():
            
            city = region[region.rfind('/')+1:].replace('_', ' ')
            for flag in flags:
                if flag["code"] == country_code:
                    emoji = flag["emoji"]
                    break
            
            tz = pytz.timezone(region)
            now = datetime.datetime.now(tz)
            response.append("{} {}: {}".format(emoji, city, now.strftime('%Y-%m-%d %H:%M:%S')))

    return '\n'.join(response)

