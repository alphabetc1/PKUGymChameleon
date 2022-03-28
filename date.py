#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime

def get_boot_date():
    date = []
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=1)

    for i in range(4):
        boot_day = (today + i * offset).strftime("%Y-%m-%d")
        date.append(boot_day)

    return date


if __name__ == '__main__': 
    date = get_boot_date()
    print(date)