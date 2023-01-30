from __future__ import annotations
import datetime

TO_MIDTOWN = "Port Imperial to Midtown"
TO_PORTIMPERIAL = "Midtown to Port Imperial"


def schedule(weekday, direction):
    interval = 20

    if direction == TO_MIDTOWN:
        if weekday in (1, 2, 3, 4, 5):
            start_time = datetime.time(6, 0)
            if weekday in (1, 2, 3, 4):
                end_time = datetime.time(22, 40)
            else:
                end_time = datetime.time(23, 40)
        elif weekday in (0, 6):
            start_time = datetime.time(8, 0)
            if weekday == 6:
                end_time = datetime.time(23, 40)
            else:  # sunday
                end_time = datetime.time(22, 40)
    else:
        if weekday in (1, 2, 3, 4, 5):
            start_time = datetime.time(6, 10)
            if weekday in (1, 2, 3, 4):
                end_time = datetime.time(22, 50)
            else:
                end_time = datetime.time(23, 50)
        elif weekday in (0, 6):
            start_time = datetime.time(8, 10)
            if weekday == 6:
                end_time = datetime.time(23, 50)
            else:  # sunday
                end_time = datetime.time(22, 50)

    return start_time, end_time, interval


def next_ferry(direction):
    current_time = datetime.datetime.now()
    weekday = current_time.weekday()

    start_time, end_time, interval = schedule(weekday=weekday, direction=direction)

    next_ferry = None
    while (next_ferry is None) or (next_ferry.time() < current_time.time()):
        next_ferry = datetime.datetime.combine(datetime.datetime.today(), start_time)
        next_ferry += datetime.timedelta(minutes=interval)
        start_time = next_ferry.time()
    if next_ferry.time() > end_time:
        return None
    else:
        return (next_ferry - datetime.datetime.now()).seconds // 60


def get_summary():
    midtown_minutes = next_ferry(TO_MIDTOWN)
    portimperial_minutes = next_ferry(TO_PORTIMPERIAL)

    return {TO_MIDTOWN: midtown_minutes, TO_PORTIMPERIAL: portimperial_minutes}
