from __future__ import annotations

import datetime

import traffic
import ferry
import bus

traffic_info = traffic.get_traffic_info()
print(traffic_info)

ferry_info = ferry.get_summary()
print(ferry_info)

bus_info = bus.get_port_imperial_bus_info()
print(bus_info)


from jinja2 import Environment, FileSystemLoader
import os

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, "templates")
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template("simple.jinja")


filename = os.path.join("./", "index.html")
print(filename)

with open(filename, "w") as fh:
    fh.write(
        template.render(
            ferry_times=ferry_info,
            tunnel_traffic=traffic_info,
            bus_info=bus_info,
            time=datetime.datetime.now().strftime("%I:%M:%S %p"),
        )
    )
