from scanner_utils import validate_ip, scan_ports
import socket

if __name__ == "__main__":
    target_ip = input("Enter the IP address or hostname to scan: ")
    
    # Validate IP address or resolve hostname
    if not validate_ip(target_ip):
        try:
            target_ip = socket.gethostbyname(target_ip)
            print(f"Resolved hostname to IP: {target_ip}")
        except socket.gaierror:
            print("Invalid IP address or hostname.")
            exit(1)
    
    port_start = int(input("Enter the starting port: "))
    port_end = int(input("Enter the ending port: "))
    
    print(f"Scanning {target_ip} for open ports from {port_start} to {port_end}...")

    open_ports = scan_ports(target_ip, (port_start, port_end))
    
    if open_ports:
        print("\nOpen Ports:")
        for port, service in open_ports:
            print(f"Port {port}: {service}")
    else:
        print("No open ports found.")
