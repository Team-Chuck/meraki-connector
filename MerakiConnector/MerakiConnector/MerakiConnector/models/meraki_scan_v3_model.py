# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = meraki_scanv3_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


class ApMAC(Enum):
    AC_17_C8_A3_A9_F8 = "ac:17:c8:a3:a9:f8"
    AC_17_C8_A3_B0_80 = "ac:17:c8:a3:b0:80"
    AC_17_C8_A3_B7_F4 = "ac:17:c8:a3:b7:f4"
    AC_17_C8_A3_BA_00 = "ac:17:c8:a3:ba:00"
    AC_17_C8_A3_BA_30 = "ac:17:c8:a3:ba:30"
    AC_17_C8_A3_BA_7_C = "ac:17:c8:a3:ba:7c"
    AC_17_C8_A3_BA_DC = "ac:17:c8:a3:ba:dc"
    AC_17_C8_A3_BD_12 = "ac:17:c8:a3:bd:12"
    AC_17_C8_A3_BD_FA = "ac:17:c8:a3:bd:fa"
    AC_17_C8_A3_BE_E6 = "ac:17:c8:a3:be:e6"


@dataclass
class LatestRecord:
    nearest_ap_rssi: Optional[int] = None
    time: Optional[datetime] = None
    nearest_ap_mac: Optional[ApMAC] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LatestRecord':
        assert isinstance(obj, dict)
        nearest_ap_rssi = from_union([from_none, lambda x: int(from_str(x))], obj.get("nearestApRssi"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        nearest_ap_mac = from_union([ApMAC, from_none], obj.get("nearestApMac"))
        return LatestRecord(nearest_ap_rssi, time, nearest_ap_mac)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nearestApRssi"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.nearest_ap_rssi)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        result["nearestApMac"] = from_union([lambda x: to_enum(ApMAC, x), from_none], self.nearest_ap_mac)
        return result


class FloorplanID(Enum):
    G_634444597505819657 = "g_634444597505819657"


class FloorplanName(Enum):
    RCDN6_4 = "RCDN6_4"


class NearestApTag(Enum):
    EMPTY = ""
    RECENTLY_ADDED = "recently-added"


@dataclass
class RssiRecord:
    ap_mac: Optional[ApMAC] = None
    rssi: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'RssiRecord':
        assert isinstance(obj, dict)
        ap_mac = from_union([ApMAC, from_none], obj.get("apMac"))
        rssi = from_union([from_int, from_none], obj.get("rssi"))
        return RssiRecord(ap_mac, rssi)

    def to_dict(self) -> dict:
        result: dict = {}
        result["apMac"] = from_union([lambda x: to_enum(ApMAC, x), from_none], self.ap_mac)
        result["rssi"] = from_union([from_int, from_none], self.rssi)
        return result


@dataclass
class Location:
    x: Optional[str] = None
    time: Optional[datetime] = None
    y: Optional[str] = None
    rssi_records: Optional[List[RssiRecord]] = None
    floorplan_name: Optional[FloorplanName] = None
    lng: Optional[float] = None
    nearest_ap_tags: Optional[List[NearestApTag]] = None
    lat: Optional[float] = None
    unc: Optional[float] = None
    floorplan_id: Optional[FloorplanID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        x = from_union([from_str, from_none], obj.get("x"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        y = from_union([from_str, from_none], obj.get("y"))
        rssi_records = from_union([lambda x: from_list(RssiRecord.from_dict, x), from_none], obj.get("rssiRecords"))
        floorplan_name = from_union([FloorplanName, from_none], obj.get("floorplanName"))
        lng = from_union([from_float, from_none], obj.get("lng"))
        nearest_ap_tags = from_union([lambda x: from_list(NearestApTag, x), from_none], obj.get("nearestApTags"))
        lat = from_union([from_float, from_none], obj.get("lat"))
        unc = from_union([from_float, from_none], obj.get("unc"))
        floorplan_id = from_union([FloorplanID, from_none], obj.get("floorplanId"))
        return Location(x, time, y, rssi_records, floorplan_name, lng, nearest_ap_tags, lat, unc, floorplan_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["x"] = from_union([from_str, from_none], self.x)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        result["y"] = from_union([from_str, from_none], self.y)
        result["rssiRecords"] = from_union([lambda x: from_list(lambda x: to_class(RssiRecord, x), x), from_none], self.rssi_records)
        result["floorplanName"] = from_union([lambda x: to_enum(FloorplanName, x), from_none], self.floorplan_name)
        result["lng"] = from_union([to_float, from_none], self.lng)
        result["nearestApTags"] = from_union([lambda x: from_list(lambda x: to_enum(NearestApTag, x), x), from_none], self.nearest_ap_tags)
        result["lat"] = from_union([to_float, from_none], self.lat)
        result["unc"] = from_union([to_float, from_none], self.unc)
        result["floorplanId"] = from_union([lambda x: to_enum(FloorplanID, x), from_none], self.floorplan_id)
        return result


class SSID(Enum):
    SS_HACK_2019 = "SS-Hack-2019"


@dataclass
class Observation:
    ipv6: None
    ipv4: Optional[str] = None
    locations: Optional[List[Location]] = None
    manufacturer: Optional[str] = None
    os: Optional[str] = None
    latest_record: Optional[LatestRecord] = None
    client_mac: Optional[str] = None
    ssid: Optional[SSID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Observation':
        assert isinstance(obj, dict)
        ipv6 = from_none(obj.get("ipv6"))
        ipv4 = from_union([from_none, from_str], obj.get("ipv4"))
        locations = from_union([lambda x: from_list(Location.from_dict, x), from_none], obj.get("locations"))
        manufacturer = from_union([from_str, from_none], obj.get("manufacturer"))
        os = from_union([from_none, from_str], obj.get("os"))
        latest_record = from_union([LatestRecord.from_dict, from_none], obj.get("latestRecord"))
        client_mac = from_union([from_str, from_none], obj.get("clientMac"))
        ssid = from_union([from_none, SSID], obj.get("ssid"))
        return Observation(ipv6, ipv4, locations, manufacturer, os, latest_record, client_mac, ssid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ipv6"] = from_none(self.ipv6)
        result["ipv4"] = from_union([from_none, from_str], self.ipv4)
        result["locations"] = from_union([lambda x: from_list(lambda x: to_class(Location, x), x), from_none], self.locations)
        result["manufacturer"] = from_union([from_str, from_none], self.manufacturer)
        result["os"] = from_union([from_none, from_str], self.os)
        result["latestRecord"] = from_union([lambda x: to_class(LatestRecord, x), from_none], self.latest_record)
        result["clientMac"] = from_union([from_str, from_none], self.client_mac)
        result["ssid"] = from_union([from_none, lambda x: to_enum(SSID, x)], self.ssid)
        return result


@dataclass
class Data:
    network_id: Optional[str] = None
    observations: Optional[List[Observation]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        network_id = from_union([from_str, from_none], obj.get("networkId"))
        observations = from_union([lambda x: from_list(Observation.from_dict, x), from_none], obj.get("observations"))
        return Data(network_id, observations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["networkId"] = from_union([from_str, from_none], self.network_id)
        result["observations"] = from_union([lambda x: from_list(lambda x: to_class(Observation, x), x), from_none], self.observations)
        return result


@dataclass
class MerakiScanv3:
    data: Optional[Data] = None
    version: Optional[str] = None
    type: Optional[str] = None
    secret: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MerakiScanv3':
        assert isinstance(obj, dict)
        data = from_union([Data.from_dict, from_none], obj.get("data"))
        version = from_union([from_str, from_none], obj.get("version"))
        type = from_union([from_str, from_none], obj.get("type"))
        secret = from_union([from_str, from_none], obj.get("secret"))
        return MerakiScanv3(data, version, type, secret)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        result["version"] = from_union([from_str, from_none], self.version)
        result["type"] = from_union([from_str, from_none], self.type)
        result["secret"] = from_union([from_str, from_none], self.secret)
        return result


def meraki_scanv3_from_dict(s: Any) -> MerakiScanv3:
    return MerakiScanv3.from_dict(s)


def meraki_scanv3_to_dict(x: MerakiScanv3) -> Any:
    return to_class(MerakiScanv3, x)