
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = meraki_scan_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Location:
    unc: Optional[float] = None
    y: Optional[List[float]] = None
    lat: Optional[float] = None
    x: Optional[List[float]] = None
    lng: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        unc = from_union([from_float, from_none], obj.get("unc"))
        y = from_union([lambda x: from_list(from_float, x), from_none], obj.get("y"))
        lat = from_union([from_float, from_none], obj.get("lat"))
        x = from_union([lambda x: from_list(from_float, x), from_none], obj.get("x"))
        lng = from_union([from_float, from_none], obj.get("lng"))
        return Location(unc, y, lat, x, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        result["unc"] = from_union([to_float, from_none], self.unc)
        result["y"] = from_union([lambda x: from_list(to_float, x), from_none], self.y)
        result["lat"] = from_union([to_float, from_none], self.lat)
        result["x"] = from_union([lambda x: from_list(to_float, x), from_none], self.x)
        result["lng"] = from_union([to_float, from_none], self.lng)
        return result


@dataclass
class Observation:
    location: Optional[Location] = None
    seen_time: Optional[datetime] = None
    seen_epoch: Optional[int] = None
    client_mac: Optional[str] = None
    rssi: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Observation':
        assert isinstance(obj, dict)
        location = from_union([Location.from_dict, from_none], obj.get("location"))
        seen_time = from_union([from_datetime, from_none], obj.get("seenTime"))
        seen_epoch = from_union([from_int, from_none], obj.get("seenEpoch"))
        client_mac = from_union([from_str, from_none], obj.get("clientMac"))
        rssi = from_union([from_int, from_none], obj.get("rssi"))
        return Observation(location, seen_time, seen_epoch, client_mac, rssi)

    def to_dict(self) -> dict:
        result: dict = {}
        result["location"] = from_union([lambda x: to_class(Location, x), from_none], self.location)
        result["seenTime"] = from_union([lambda x: x.isoformat(), from_none], self.seen_time)
        result["seenEpoch"] = from_union([from_int, from_none], self.seen_epoch)
        result["clientMac"] = from_union([from_str, from_none], self.client_mac)
        result["rssi"] = from_union([from_int, from_none], self.rssi)
        return result


@dataclass
class Data:
    observations: Optional[List[Observation]] = None
    ap_mac: Optional[str] = None
    ap_floors: Optional[List[str]] = None
    ap_tags: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        observations = from_union([lambda x: from_list(Observation.from_dict, x), from_none], obj.get("observations"))
        ap_mac = from_union([from_str, from_none], obj.get("apMac"))
        ap_floors = from_union([lambda x: from_list(from_str, x), from_none], obj.get("apFloors"))
        ap_tags = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("apTags"))
        return Data(observations, ap_mac, ap_floors, ap_tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["observations"] = from_union([lambda x: from_list(lambda x: to_class(Observation, x), x), from_none], self.observations)
        result["apMac"] = from_union([from_str, from_none], self.ap_mac)
        result["apFloors"] = from_union([lambda x: from_list(from_str, x), from_none], self.ap_floors)
        result["apTags"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.ap_tags)
        return result


@dataclass
class MerakiScan:
    secret: Optional[str] = None
    type: Optional[str] = None
    data: Optional[Data] = None
    version: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MerakiScan':
        assert isinstance(obj, dict)
        secret = from_union([from_str, from_none], obj.get("secret"))
        type = from_union([from_str, from_none], obj.get("type"))
        data = from_union([Data.from_dict, from_none], obj.get("data"))
        version = from_union([from_str, from_none], obj.get("version"))
        return MerakiScan(secret, type, data, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["secret"] = from_union([from_str, from_none], self.secret)
        result["type"] = from_union([from_str, from_none], self.type)
        result["data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        result["version"] = from_union([from_str, from_none], self.version)
        return result


def meraki_scan_from_dict(s: Any) -> MerakiScan:
    return MerakiScan.from_dict(s)


def meraki_scan_to_dict(x: MerakiScan) -> Any:
    return to_class(MerakiScan, x)
