# weekday schedule
# Port Imperial to Midtown:  ferry runs from 6 am to 10:40 pm, with departures every 20 minutes.  On Friday, it extends to 11:40 pm
# Midtown to Port Imperial:  ferry runs from 6:10 am to 10:50 pm, with departures every 20 minutes.  On Friday, it extends until 11:50 pm

# weekend schedule
# Port Imperial to Midtown:  ferry runs from 8 am to 10:40 pm, with departures every 20 minutes.  On Saturday, it extends to 11:40 pm
# Midtown to Port Imperial:  ferry runs from 8:10 am to 10:50 pm, with departures every 20 minutes.  On Saturday, it extends to 11:50 pm

# entirely written using ChatGPT

from __future__ import annotations

from datetime import datetime, timedelta
from dataclasses import dataclass
import json


@dataclass
class FerryInfo:
    direction: str
    travelTime: int

    def __repr__(self):
        return f"{self.direction}: {self.travelTime} minutes"


weekday_schedule = {
    "Port Imperial to Midtown": {
        "start_time": "6:00 AM",
        "end_time": "10:40 PM",
        "interval": 20,
        "special_end_time": "11:40 PM",  # friday
    },
    "Midtown to Port Imperial": {
        "start_time": "6:10 AM",
        "end_time": "10:50 PM",
        "interval": 20,
        "special_end_time": "11:50 PM",
    },
}

weekend_schedule = {
    "Port Imperial to Midtown": {
        "start_time": "8:00 AM",
        "end_time": "10:40 PM",
        "interval": 20,
        "special_end_time": "11:40 PM",  # saturday
    },
    "Midtown to Port Imperial": {
        "start_time": "8:10 AM",
        "end_time": "10:50 PM",
        "interval": 20,
        "special_end_time": "11:50 PM",
    },
}


def get_next_ferry_time(schedule, direction, timeobj):
    current_day = timeobj.weekday()

    start_time = datetime.strptime(schedule[direction]["start_time"], "%I:%M %p").time()
    end_time = datetime.strptime(schedule[direction]["end_time"], "%I:%M %p").time()
    interval = timedelta(minutes=schedule[direction]["interval"])
    if current_day in (4, 5):
        end_time = datetime.strptime(schedule[direction]["special_end_time"], "%I:%M %p").time()

    next_ferry = None
    while (next_ferry is None) or (next_ferry.time() < timeobj.time()):
        next_ferry = datetime.combine(datetime.today(), start_time)
        next_ferry += interval
        start_time = next_ferry.time()
    if next_ferry.time() > end_time:
        return None
    else:
        return (next_ferry - datetime.now()).seconds // 60


# Example usage
# print("Next Port Imperial to Midtown ferry: " + str(get_next_ferry_time(weekday_schedule if datetime.today().weekday() < 5 else weekend_schedule, "Port Imperial to Midtown")) + " minutes")
# print("Next Midtown to Port Imperial ferry: " + str(get_next_ferry_time(weekday_schedule if datetime.today().weekday() < 5 else weekend_schedule, "Midtown to Port Imperial")) + " minutes")


def get_port_imperial_times():

    timeobj = datetime.now()

    pi_midtown_minutes = get_next_ferry_time(
        weekday_schedule if datetime.today().weekday() < 5 else weekend_schedule, "Port Imperial to Midtown", timeobj
    )
    midtown_pi_minutes = get_next_ferry_time(
        weekday_schedule if datetime.today().weekday() < 5 else weekend_schedule, "Midtown to Port Imperial", timeobj
    )

    pi_midtown = FerryInfo("Port Imperial to Midtown", pi_midtown_minutes)
    midtown_pi = FerryInfo("Midtown to Port Imperial", midtown_pi_minutes)

    return pi_midtown, midtown_pi
