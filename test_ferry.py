import pytest
import datetime
from ferry import next_ferry, schedule

def test_next_ferry():
    current_time = datetime.datetime.now()
    direction = "Port Imperial to Midtown"
    
    # Test during weekday with service to midtown
    result = next_ferry(current_time, direction)
    assert result is not None
    
    direction = "Midtown to Port Imperial"
    # Test during weekday with service to Port Imperial
    result = next_ferry(current_time, direction)
    assert result is not None
    
    # Test during weekend with service to midtown
    current_time = datetime.datetime(2023, 1, 29)
    result = next_ferry(current_time, direction)
    assert result is not None
    
    # Test during weekend with service to Port Imperial
    direction = "Midtown to Port Imperial"
    result = next_ferry(current_time, direction)
    assert result is not None
    
    # Test outside of service hours
    current_time = datetime.datetime(2023, 1, 29, 23, 59)
    result = next_ferry(current_time, direction)
    assert result is None

def test_schedule():
    weekday = 1
    direction = "Port Imperial to Midtown"
    
    # Test schedule for weekday with service to midtown
    start_time, end_time, interval = schedule(weekday, direction)
    assert start_time == datetime.time(6, 0)
    assert end_time == datetime.time(22, 40)
    assert interval == 20
    
    direction = "Midtown to Port Imperial"
    # Test schedule for weekday with service to Port Imperial
    start_time, end_time, interval = schedule(weekday, direction)
    assert start_time == datetime.time(6, 10)
    assert end_time == datetime.time(22, 50)
    assert interval == 20
    
    weekday = 6
    direction = "Port Imperial to Midtown"
    # Test schedule for weekend with service to midtown
    start_time, end_time, interval = schedule(weekday, direction)
    assert start_time == datetime.time(8, 0)
    assert end_time == datetime.time(23, 40)
    assert interval == 20
    
    direction = "Midtown to Port Imperial"
    # Test schedule for weekend with service to Port Imperial
    start_time, end_time, interval = schedule(weekday, direction)
    assert start_time == datetime.time(8, 10)
    assert end_time == datetime.time(23, 50)
    assert interval == 20
