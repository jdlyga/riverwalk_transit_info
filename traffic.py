from __future__ import annotations

import httpx
from dataclasses import dataclass


@dataclass
class TrafficInfo:
    travelDirection: str
    routeSpeed: int
    travelTime: int
    timeStamp: str
    infomationalText: str

    def pretty_direction(self):
        if self.travelDirection == "ToNJ":
            return "Tunnel to New Jersey"
        else:
            return "Tunnel to Midtown"

    def __repr__(self):
        return f"{self.pretty_direction()} bound traffic is moving at {self.routeSpeed} mph and the estimated travel time is {self.travelTime} minutes as of {self.timeStamp}. Additional information: {self.infomationalText}"


def get_traffic_info() -> list[TrafficInfo]:
    response = httpx.get("https://www.panynj.gov/bin/portauthority/crossingtimesapi.json")

    port_authority_json = response.json()

    def parse_traffic_times(json):
        for element in json:
            if element["crossingDisplayName"] == "Lincoln Tunnel":
                yield TrafficInfo(
                    element["travelDirection"],
                    element["routeSpeed"],
                    element["routeTravelTime"],
                    element["timeStamp"],
                    element["infomationalText"].capitalize(),
                )

    info = list(parse_traffic_times(port_authority_json))
    info.reverse()  # so midtown is first
    return info
