import pytz

def get_entry_date(creation_date, time_zone):
    tz = pytz.timezone(time_zone)
    result = pytz.utc.localize(creation_date).astimezone(tz)
    #info('%s, %s -> %s, %d, %d' % (creation_date, time_zone, result, result.hour, result.minute))
    return result
