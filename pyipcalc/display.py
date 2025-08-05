"""Display formatting utilities for IP calculator."""

from typing import Union
from .models import IPv4Info, IPv6Info


class DisplayFormatter:
    """Format IP calculation results for display."""
    
    @staticmethod
    def format_ipv4_output(info: IPv4Info) -> str:
        """Format IPv4 information for display."""
        output = []
        
        # Network Information
        output.append("=== IPv4 Network Information ===")
        output.append(f"Network:           {info.network}/{info.prefix_length}")
        output.append(f"Netmask:           {info.netmask}")
        output.append(f"Wildcard:          {info.wildcard}")
        if info.broadcast:
            output.append(f"Broadcast:         {info.broadcast}")
        output.append(f"Network Class:     {info.network_class}")
        output.append("")
        
        # Host Range
        output.append("=== Host Range ===")
        output.append(f"First Host:        {info.first_host}")
        output.append(f"Last Host:         {info.last_host}")
        output.append(f"Total Hosts:       {info.total_hosts:,}")
        output.append(f"Usable Hosts:      {info.usable_hosts:,}")
        output.append("")
        
        # Hexadecimal Format
        output.append("=== Hexadecimal Format ===")
        output.append(f"Network (Hex):     {info.network_hex}")
        output.append(f"Netmask (Hex):     {info.netmask_hex}")
        if info.broadcast:
            output.append(f"Broadcast (Hex):   {info.broadcast_hex}")
        output.append(f"First Host (Hex):  {info.first_host_hex}")
        output.append(f"Last Host (Hex):   {info.last_host_hex}")
        output.append("")
        
        # Binary Format
        output.append("=== Binary Format ===")
        output.append(f"Network (Binary):  {info.binary_network}")
        output.append(f"Netmask (Binary):  {info.binary_netmask}")
        output.append("")
        
        # Possible Subnets
        if info.possible_subnets:
            output.append("=== Possible Subnet Divisions ===")
            for subnet in info.possible_subnets:
                output.append(f"  {subnet}")
            output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def format_ipv6_output(info: IPv6Info) -> str:
        """Format IPv6 information for display."""
        output = []
        
        # Network Information
        output.append("=== IPv6 Network Information ===")
        output.append(f"Network:           {info.network}/{info.prefix_length}")
        output.append(f"Prefix Length:     /{info.prefix_length}")
        output.append("")
        
        # Address Formats
        output.append("=== Address Formats ===")
        output.append(f"Compressed:        {info.compressed}")
        output.append(f"Expanded:          {info.expanded}")
        output.append(f"Hexadecimal:       {info.network_hex}")
        output.append("")
        
        # Host Range
        output.append("=== Host Range ===")
        output.append(f"First Host:        {info.first_host}")
        output.append(f"Last Host:         {info.last_host}")
        if info.total_hosts < 2**64:
            output.append(f"Total Hosts:       {info.total_hosts:,}")
        else:
            output.append(f"Total Hosts:       {info.total_hosts} (2^{128-info.prefix_length})")
        output.append("")
        
        # Possible Subnets
        if info.possible_subnets:
            output.append("=== Possible Subnet Divisions ===")
            for subnet in info.possible_subnets:
                output.append(f"  {subnet}")
            output.append("")
        
        return "\n".join(output)
    
    @classmethod
    def format_output(cls, info: Union[IPv4Info, IPv6Info]) -> str:
        """Format output based on IP version."""
        if isinstance(info, IPv4Info):
            return cls.format_ipv4_output(info)
        else:
            return cls.format_ipv6_output(info)
