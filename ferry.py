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


def next_ferry(current_time, direction):
    weekday = current_time.weekday()
    start_time, end_time, interval = schedule(weekday=weekday, direction=direction)

    next_ferry = datetime.datetime.combine(datetime.datetime.today(), start_time)

    if current_time.time() > end_time or current_time.time() < start_time:
        return None, None

    while next_ferry < current_time:
        next_ferry += datetime.timedelta(minutes=interval)

    minutes = (next_ferry - current_time).seconds // 60
    time = next_ferry.strftime("%-I:%M %p")
    return minutes, time


def get_summary():
    current_time = datetime.datetime.now()
    midtown_minutes, midtown_time = next_ferry(current_time, TO_MIDTOWN)
    portimperial_minutes, portimperial_time = next_ferry(current_time, TO_PORTIMPERIAL)

    return {
        TO_MIDTOWN: {"minutes": midtown_minutes, "time": midtown_time},
        TO_PORTIMPERIAL: {"minutes": portimperial_minutes, "time": portimperial_time},
    }
