
def _iso_time_format(dt):
    return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, int(dt.microsecond / 1000))

