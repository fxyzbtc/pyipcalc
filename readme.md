# PyIPCalc

A comprehensive utility to calculate IPv4 and IPv6 network information with support for multiple input formats and detailed output including hexadecimal representations and subnet possibilities.

## Features

- **IPv4 Support**: Calculate network information for IPv4 addresses
- **IPv6 Support**: Full IPv6 network calculation support
- **Multiple Input Formats**: 
  - CIDR notation (192.168.1.0/24, 2001:db8::/32)
  - Decimal netmask (192.168.1.0/255.255.255.0)
  - IPv6 compressed format (::1, ::ffff:192.168.1.1)
- **Comprehensive Output**:
  - Network, broadcast, and host range information
  - Hexadecimal and binary representations (IPv4)
  - Possible subnet divisions
  - Network class information (IPv4)
- **Multiple Usage Options**: Command-line script, Python module, or `python -m` execution

## Installation

```bash
pip install pyipcalc
```

For development:

```bash
git clone https://github.com/fxyzbtc/pyipcalc.git
cd pyipcalc
uv install
```

## Usage

### As a Command-Line Tool

```bash
# IPv4 with CIDR notation
pyipcalc 192.168.1.0/24

# IPv4 with decimal netmask
pyipcalc 192.168.1.0/255.255.255.0

# IPv6 network
pyipcalc 2001:db8::/32

# With verbose output
pyipcalc -v 10.0.0.0/8

# Quiet mode (results only)
pyipcalc -q 172.16.0.0/12
```

### As a Python Module

```bash
python -m pyipcalc 192.168.1.0/24
```

### In Python Code

```python
from pyipcalc import IPCalculator, DisplayFormatter

# Calculate network information
result = IPCalculator.calculate("192.168.1.0/24")

# Display formatted output
print(DisplayFormatter.format_output(result))

# Access specific information
print(f"Network: {result.network}")
print(f"Usable hosts: {result.usable_hosts}")
print(f"Hexadecimal: {result.network_hex}")
```

## Output Examples

### IPv4 Example

```
=== IPv4 Network Information ===
Network:           192.168.1.0/24
Netmask:           255.255.255.0
Wildcard:          0.0.0.255
Broadcast:         192.168.1.255
Network Class:     C

=== Host Range ===
First Host:        192.168.1.1
Last Host:         192.168.1.254
Total Hosts:       256
Usable Hosts:      254

=== Hexadecimal Format ===
Network (Hex):     C0.A8.01.00
Netmask (Hex):     FF.FF.FF.00
Broadcast (Hex):   C0.A8.01.FF
First Host (Hex):  C0.A8.01.01
Last Host (Hex):   C0.A8.01.FE

=== Binary Format ===
Network (Binary):  11000000.10101000.00000001.00000000
Netmask (Binary):  11111111.11111111.11111111.00000000

=== Possible Subnet Divisions ===
  /25 (2 subnets)
  /26 (4 subnets)
  /27 (8 subnets)
  /28 (16 subnets)
  /29 (32 subnets)
  /30 (64 subnets)
```

### IPv6 Example

```
=== IPv6 Network Information ===
Network:           2001:db8::/32
Prefix Length:     /32

=== Address Formats ===
Compressed:        2001:db8::
Expanded:          2001:0db8:0000:0000:0000:0000:0000:0000
Hexadecimal:       20010db8000000000000000000000000

=== Host Range ===
First Host:        2001:db8::
Last Host:         2001:db8:ffff:ffff:ffff:ffff:ffff:ffff
Total Hosts:       79,228,162,514,264,337,593,543,950,336

=== Possible Subnet Divisions ===
  /48 (65536 subnets)
  /56 (16777216 subnets)
  /60 (268435456 subnets)
  /64 (4294967296 subnets)
```

## Supported Input Formats

- **IPv4 CIDR**: `192.168.1.0/24`
- **IPv4 with decimal netmask**: `192.168.1.0/255.255.255.0`
- **IPv6 CIDR**: `2001:db8::/32`
- **IPv6 compressed**: `::1/128`, `::ffff:192.168.1.1/96`
- **Single IP addresses**: Automatically assumes `/32` for IPv4 and `/128` for IPv6

## Development

### Setup Development Environment

```bash
git clone https://github.com/fxyzbtc/pyipcalc.git
cd pyipcalc
uv venv
uv install
```

### Running Tests

```bash
uv run pytest
```

### Code Style

This project uses `ruff` for code formatting and linting:

```bash
uv run ruff check
uv run ruff format
```

## Pain Points Solved

- **Multiple Format Support**: No need to convert between different IP notation formats
- **Comprehensive Information**: Get all network details in one command
- **Hexadecimal Output**: Essential for network programming and debugging
- **Subnet Planning**: See possible subnet divisions at a glance
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multiple Interfaces**: Use as CLI tool, Python module, or import in code

## Links

- **Homepage**: [https://github.com/fxyzbtc/pyipcalc](https://github.com/fxyzbtc/pyipcalc)
- **Documentation**: [https://deepwiki.com/fxyzbtc/pyipcalc](https://deepwiki.com/fxyzbtc/pyipcalc)
- **Issues**: [https://github.com/fxyzbtc/pyipcalc/issues](https://github.com/fxyzbtc/pyipcalc/issues)
- **PyPI**: [https://pypi.org/project/pyipcalc/](https://pypi.org/project/pyipcalc/)

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.