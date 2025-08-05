"""IP Calculator utility functions."""

import ipaddress
from typing import List, Union, Tuple
from loguru import logger

from .models import IPv4Info, IPv6Info, get_ipv4_class


class IPCalculator:
    """Main IP calculator class."""
    
    @staticmethod
    def parse_input(ip_input: str) -> Tuple[Union[ipaddress.IPv4Network, ipaddress.IPv6Network], str]:
        """Parse various IP input formats."""
        ip_input = ip_input.strip()
        
        # Handle IPv4 with decimal netmask (e.g., 192.168.1.0/255.255.255.0)
        if '/' in ip_input and '.' in ip_input.split('/')[1]:
            ip_part, netmask_part = ip_input.split('/', 1)
            try:
                # Convert decimal netmask to CIDR
                netmask = ipaddress.IPv4Address(netmask_part)
                prefix_length = sum(bin(int(octet)).count('1') for octet in str(netmask).split('.'))
                network = ipaddress.IPv4Network(f"{ip_part}/{prefix_length}", strict=False)
                return network, "IPv4"
            except ipaddress.AddressValueError:
                pass
        
        try:
            # Try parsing as IPv4 network
            if ':' not in ip_input:
                network = ipaddress.IPv4Network(ip_input, strict=False)
                return network, "IPv4"
            else:
                # Try parsing as IPv6 network
                network = ipaddress.IPv6Network(ip_input, strict=False)
                return network, "IPv6"
        except ipaddress.AddressValueError as e:
            logger.error(f"Invalid IP address format: {ip_input}")
            raise ValueError(f"Invalid IP address format: {ip_input}") from e
    
    @staticmethod
    def calculate_ipv4(network: ipaddress.IPv4Network) -> IPv4Info:
        """Calculate IPv4 network information."""
        logger.info(f"Calculating IPv4 info for {network}")
        
        # Basic network information
        total_hosts = network.num_addresses
        usable_hosts = max(0, total_hosts - 2) if network.prefixlen < 31 else total_hosts
        
        # Get addresses
        network_addr = network.network_address
        broadcast_addr = network.broadcast_address
        
        if network.prefixlen < 31:
            first_host = network_addr + 1
            last_host = broadcast_addr - 1
        else:
            # /31 and /32 networks
            first_host = network_addr
            last_host = broadcast_addr
        
        # Hex representations
        def ip_to_hex(ip: ipaddress.IPv4Address) -> str:
            return '.'.join(f"{int(octet):02X}" for octet in str(ip).split('.'))
        
        # Binary representations
        def ip_to_binary(ip: ipaddress.IPv4Address) -> str:
            return '.'.join(f"{int(octet):08b}" for octet in str(ip).split('.'))
        
        # Calculate possible subnets
        possible_subnets = IPCalculator._generate_ipv4_subnets(network)
        
        return IPv4Info(
            network=str(network.network_address),
            prefix_length=network.prefixlen,
            netmask=str(network.netmask),
            wildcard=str(network.hostmask),
            broadcast=str(broadcast_addr) if network.prefixlen < 31 else None,
            first_host=str(first_host),
            last_host=str(last_host),
            total_hosts=total_hosts,
            usable_hosts=usable_hosts,
            network_class=get_ipv4_class(network_addr),
            network_hex=ip_to_hex(network_addr),
            netmask_hex=ip_to_hex(network.netmask),
            broadcast_hex=ip_to_hex(broadcast_addr),
            first_host_hex=ip_to_hex(first_host),
            last_host_hex=ip_to_hex(last_host),
            binary_network=ip_to_binary(network_addr),
            binary_netmask=ip_to_binary(network.netmask),
            possible_subnets=possible_subnets
        )
    
    @staticmethod
    def calculate_ipv6(network: ipaddress.IPv6Network) -> IPv6Info:
        """Calculate IPv6 network information."""
        logger.info(f"Calculating IPv6 info for {network}")
        
        # Basic network information
        total_hosts = network.num_addresses
        usable_hosts = total_hosts  # IPv6 doesn't reserve broadcast
        
        # Get addresses
        network_addr = network.network_address
        last_addr = network.broadcast_address
        first_host = network_addr
        last_host = last_addr
        
        # IPv6 specific formatting
        compressed = str(network_addr.compressed)
        expanded = str(network_addr.exploded)
        network_hex = network_addr.exploded.replace(':', '')
        
        # Calculate possible subnets
        possible_subnets = IPCalculator._generate_ipv6_subnets(network)
        
        return IPv6Info(
            network=str(network_addr),
            prefix_length=network.prefixlen,
            netmask=f"/{network.prefixlen}",
            wildcard="N/A",  # IPv6 doesn't use wildcard masks
            broadcast=None,  # IPv6 doesn't have broadcast
            first_host=str(first_host),
            last_host=str(last_host),
            total_hosts=total_hosts,
            usable_hosts=usable_hosts,
            network_hex=network_hex,
            compressed=compressed,
            expanded=expanded,
            possible_subnets=possible_subnets
        )
    
    @staticmethod
    def _generate_ipv4_subnets(network: ipaddress.IPv4Network) -> List[str]:
        """Generate possible subnet divisions for IPv4."""
        subnets = []
        current_prefix = network.prefixlen
        
        # Generate subnets by increasing prefix length
        for prefix_len in range(current_prefix + 1, min(current_prefix + 9, 31)):
            try:
                subnet_count = 2 ** (prefix_len - current_prefix)
                subnets.append(f"/{prefix_len} ({subnet_count} subnets)")
            except ValueError:
                break
        
        return subnets[:8]  # Limit to 8 entries
    
    @staticmethod
    def _generate_ipv6_subnets(network: ipaddress.IPv6Network) -> List[str]:
        """Generate possible subnet divisions for IPv6."""
        subnets = []
        current_prefix = network.prefixlen
        
        # Common IPv6 subnet boundaries with special handling
        important_prefixes = [48, 56, 60, 64]  # Most common IPv6 subnet sizes
        
        for prefix_len in important_prefixes:
            if prefix_len > current_prefix and prefix_len <= 128:
                subnet_count = 2 ** (prefix_len - current_prefix)
                
                if subnet_count <= 65536:
                    subnets.append(f"/{prefix_len} ({subnet_count} subnets)")
                elif subnet_count <= 2**20:  # Up to ~1M
                    k_count = subnet_count // 1024
                    subnets.append(f"/{prefix_len} ({k_count}K subnets)")
                elif subnet_count <= 2**30:  # Up to ~1B
                    m_count = subnet_count // (1024 * 1024)
                    subnets.append(f"/{prefix_len} ({m_count}M subnets)")
                else:
                    # For very large counts, use scientific notation
                    exp = prefix_len - current_prefix
                    subnets.append(f"/{prefix_len} (2^{exp} subnets)")
        
        # Add a few more if we have room
        additional_prefixes = [72, 80, 96, 112]
        for prefix_len in additional_prefixes:
            if len(subnets) >= 6:  # Limit total entries
                break
            if prefix_len > current_prefix and prefix_len <= 128:
                exp = prefix_len - current_prefix
                subnets.append(f"/{prefix_len} (2^{exp} subnets)")
        
        return subnets[:8]  # Limit to 8 entries
    
    @classmethod
    def calculate(cls, ip_input: str) -> Union[IPv4Info, IPv6Info]:
        """Main calculation method."""
        network, ip_type = cls.parse_input(ip_input)
        
        if ip_type == "IPv4":
            return cls.calculate_ipv4(network)
        else:
            return cls.calculate_ipv6(network)
