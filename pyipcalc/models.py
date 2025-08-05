"""Data models for IP calculator."""

from typing import List, Optional
from dataclasses import dataclass
from ipaddress import IPv4Address


@dataclass
class NetworkInfo:
    """Base class for network information."""
    network: str
    prefix_length: int
    netmask: str
    wildcard: str
    broadcast: Optional[str]
    first_host: str
    last_host: str
    total_hosts: int
    usable_hosts: int
    network_class: Optional[str] = None


@dataclass
class IPv4Info(NetworkInfo):
    """IPv4 network information."""
    network_hex: str = ""
    netmask_hex: str = ""
    broadcast_hex: str = ""
    first_host_hex: str = ""
    last_host_hex: str = ""
    binary_network: str = ""
    binary_netmask: str = ""
    possible_subnets: List[str] = None
    
    def __post_init__(self):
        if self.possible_subnets is None:
            self.possible_subnets = []


@dataclass
class IPv6Info(NetworkInfo):
    """IPv6 network information."""
    network_hex: str = ""
    compressed: str = ""
    expanded: str = ""
    possible_subnets: List[str] = None
    
    def __post_init__(self):
        if self.possible_subnets is None:
            self.possible_subnets = []


def get_ipv4_class(address: IPv4Address) -> str:
    """Determine IPv4 address class."""
    first_octet = int(str(address).split('.')[0])
    
    if 1 <= first_octet <= 126:
        return "A"
    elif first_octet == 127:
        return "A (Loopback)"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    elif 224 <= first_octet <= 239:
        return "D (Multicast)"
    elif 240 <= first_octet <= 255:
        return "E (Reserved)"
    else:
        return "Unknown"
