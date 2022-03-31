import datetime

def get_boot_date(st, ed):
    now = datetime.datetime.now()
    offset = datetime.timedelta(days=1)
    if now.hour < 12:
        ed = min(ed, 2)
    date = []

    for i in range(ed, st - 1, -1):
        boot_day = (now + i * offset).strftime("%Y-%m-%d")
        date.append(boot_day)

    return date


def seconds_till_twelve():
    now = datetime.datetime.now()
    return abs((12 - now.hour) * 3600 - now.minute * 60 - now.second)


if __name__ == '__main__':
    print(seconds_till_twelve())