import socket
from concurrent.futures import ThreadPoolExecutor
from common_ports import common_ports

def scan_port(ip, port):
    """Attempt to connect to a specified port on the IP address."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        sock.connect((ip, port))
        service = common_ports.get(port, 'Unknown Service')
        return port, service  # Return port and service if open
    except:
        return None  # Port is closed or filtered
    finally:
        sock.close()

def scan_ports(ip, port_range=(1, 1024)):
    """Scan a range of ports on the target IP address."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda port: scan_port(ip, port), range(port_range[0], port_range[1]+1))
        for result in results:
            if result:
                open_ports.append(result)
    return open_ports

def validate_ip(ip):
    """Validate the IP address format."""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False