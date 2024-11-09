import socket
from concurrent.futures import ThreadPoolExecutor
import subprocess
from common_ports import common_ports

def scan_port(ip, port):
    """Attempt to connect to a specified port on the IP address and get service name."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        sock.connect((ip, port))
        
        # Attempt to retrieve the service name for the port
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = common_ports.get(port, 'Unknown Service')  # Use custom service name or default
        
        process_info = get_process_info(port)  # Get process info for open ports
        return port, service, process_info
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

def get_process_info(port):
    """Get process information for a given open port using lsof or netstat."""
    try:
        # Using lsof to get the process info on Unix systems
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        
        if result.stdout:
            # Return only the first line of process information for simplicity
            return result.stdout.splitlines()[1]  # Skipping header line
        else:
            return "No process info available"  # If no process found
    except FileNotFoundError:
        # If `lsof` is not available, try using `netstat`
        result = subprocess.run(['netstat', '-anp', 'tcp'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if f'.{port} ' in line:
                return line  # Return matching line with port info
        return "No process info available"
