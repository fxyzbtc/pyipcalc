"""Tests for pyipcalc package."""

import pytest
import ipaddress
from pyipcalc import IPCalculator, IPv4Info, IPv6Info
from pyipcalc.display import DisplayFormatter


class TestIPCalculator:
    """Test the IPCalculator class."""
    
    def test_parse_ipv4_cidr(self):
        """Test parsing IPv4 CIDR notation."""
        network, ip_type = IPCalculator.parse_input("192.168.1.0/24")
        assert ip_type == "IPv4"
        assert isinstance(network, ipaddress.IPv4Network)
        assert str(network) == "192.168.1.0/24"
    
    def test_parse_ipv4_decimal_netmask(self):
        """Test parsing IPv4 with decimal netmask."""
        network, ip_type = IPCalculator.parse_input("192.168.1.0/255.255.255.0")
        assert ip_type == "IPv4"
        assert isinstance(network, ipaddress.IPv4Network)
        assert network.prefixlen == 24
    
    def test_parse_ipv6_cidr(self):
        """Test parsing IPv6 CIDR notation."""
        network, ip_type = IPCalculator.parse_input("2001:db8::/32")
        assert ip_type == "IPv6"
        assert isinstance(network, ipaddress.IPv6Network)
        assert str(network) == "2001:db8::/32"
    
    def test_parse_ipv6_compressed(self):
        """Test parsing IPv6 compressed format."""
        network, ip_type = IPCalculator.parse_input("::1/128")
        assert ip_type == "IPv6"
        assert isinstance(network, ipaddress.IPv6Network)
        assert network.prefixlen == 128
    
    def test_invalid_input(self):
        """Test handling of invalid input."""
        with pytest.raises(ValueError):
            IPCalculator.parse_input("invalid.ip.address")
    
    def test_calculate_ipv4_class_c(self):
        """Test IPv4 calculation for Class C network."""
        result = IPCalculator.calculate("192.168.1.0/24")
        assert isinstance(result, IPv4Info)
        assert result.network == "192.168.1.0"
        assert result.prefix_length == 24
        assert result.netmask == "255.255.255.0"
        assert result.broadcast == "192.168.1.255"
        assert result.first_host == "192.168.1.1"
        assert result.last_host == "192.168.1.254"
        assert result.total_hosts == 256
        assert result.usable_hosts == 254
        assert result.network_class == "C"
    
    def test_calculate_ipv4_hex_format(self):
        """Test IPv4 hexadecimal formatting."""
        result = IPCalculator.calculate("192.168.1.0/24")
        assert result.network_hex == "C0.A8.01.00"
        assert result.netmask_hex == "FF.FF.FF.00"
        assert result.broadcast_hex == "C0.A8.01.FF"
    
    def test_calculate_ipv4_binary_format(self):
        """Test IPv4 binary formatting."""
        result = IPCalculator.calculate("192.168.1.0/24")
        assert "11000000.10101000.00000001.00000000" in result.binary_network
        assert "11111111.11111111.11111111.00000000" in result.binary_netmask
    
    def test_calculate_ipv4_host_only_network(self):
        """Test IPv4 /32 network (single host)."""
        result = IPCalculator.calculate("192.168.1.1/32")
        assert result.total_hosts == 1
        assert result.usable_hosts == 1
        assert result.first_host == "192.168.1.1"
        assert result.last_host == "192.168.1.1"
        assert result.broadcast is None
    
    def test_calculate_ipv4_point_to_point(self):
        """Test IPv4 /31 network (point-to-point)."""
        result = IPCalculator.calculate("192.168.1.0/31")
        assert result.total_hosts == 2
        assert result.usable_hosts == 2
        assert result.first_host == "192.168.1.0"
        assert result.last_host == "192.168.1.1"
        assert result.broadcast is None
    
    def test_calculate_ipv6_basic(self):
        """Test IPv6 calculation."""
        result = IPCalculator.calculate("2001:db8::/32")
        assert isinstance(result, IPv6Info)
        assert result.network == "2001:db8::"
        assert result.prefix_length == 32
        assert result.compressed == "2001:db8::"
        assert result.expanded == "2001:0db8:0000:0000:0000:0000:0000:0000"
    
    def test_calculate_ipv6_subnets(self):
        """Test IPv6 subnet generation."""
        result = IPCalculator.calculate("2001:db8::/32")
        assert len(result.possible_subnets) > 0
        assert any("/48" in subnet for subnet in result.possible_subnets)
        assert any("/64" in subnet for subnet in result.possible_subnets)
    
    def test_ipv4_subnets_generation(self):
        """Test IPv4 subnet generation."""
        result = IPCalculator.calculate("192.168.0.0/16")
        assert len(result.possible_subnets) > 0
        assert any("/17" in subnet for subnet in result.possible_subnets)
        assert any("/24" in subnet for subnet in result.possible_subnets)


class TestDisplayFormatter:
    """Test the DisplayFormatter class."""
    
    def test_format_ipv4_output(self):
        """Test IPv4 output formatting."""
        result = IPCalculator.calculate("192.168.1.0/24")
        output = DisplayFormatter.format_output(result)
        
        assert "IPv4 Network Information" in output
        assert "192.168.1.0/24" in output
        assert "255.255.255.0" in output
        assert "Host Range" in output
        assert "Hexadecimal Format" in output
        assert "Binary Format" in output
        assert "Possible Subnet Divisions" in output
    
    def test_format_ipv6_output(self):
        """Test IPv6 output formatting."""
        result = IPCalculator.calculate("2001:db8::/32")
        output = DisplayFormatter.format_output(result)
        
        assert "IPv6 Network Information" in output
        assert "2001:db8::/32" in output
        assert "Address Formats" in output
        assert "Compressed:" in output
        assert "Expanded:" in output
        assert "Hexadecimal:" in output
    
    def test_format_ipv4_no_broadcast(self):
        """Test IPv4 formatting without broadcast (e.g., /31, /32)."""
        result = IPCalculator.calculate("192.168.1.1/32")
        output = DisplayFormatter.format_output(result)
        
        # Should not contain broadcast information for /32
        assert "Broadcast:" not in output or "None" in output


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_loopback_ipv4(self):
        """Test IPv4 loopback address."""
        result = IPCalculator.calculate("127.0.0.1/8")
        assert result.network_class == "A"
        assert result.network == "127.0.0.0"
    
    def test_loopback_ipv6(self):
        """Test IPv6 loopback address."""
        result = IPCalculator.calculate("::1/128")
        assert result.network == "::1"
        assert result.total_hosts == 1
    
    def test_multicast_ipv4(self):
        """Test IPv4 multicast address."""
        result = IPCalculator.calculate("224.0.0.1/24")
        assert "Multicast" in result.network_class
    
    def test_large_ipv4_network(self):
        """Test large IPv4 network."""
        result = IPCalculator.calculate("10.0.0.0/8")
        assert result.network_class == "A"
        assert result.total_hosts == 16777216
        assert result.usable_hosts == 16777214
    
    def test_small_ipv6_network(self):
        """Test small IPv6 network."""
        result = IPCalculator.calculate("2001:db8::1/127")
        assert result.total_hosts == 2
        assert result.prefix_length == 127


if __name__ == "__main__":
    pytest.main([__file__])
