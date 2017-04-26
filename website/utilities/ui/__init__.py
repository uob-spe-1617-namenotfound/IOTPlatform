import datetime


def timestamp_to_date_time(timestamp):
    dt = datetime.datetime.fromtimestamp(float(timestamp))
    return dt.strftime("%Y-%m-%d %H:%M")
