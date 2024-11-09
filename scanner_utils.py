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