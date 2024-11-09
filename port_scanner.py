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
    
    print(f"\nScanning {target_ip} for open ports from {port_start} to {port_end}...\n")
    
    open_ports = scan_ports(target_ip, (port_start, port_end))
    
    if open_ports:
        print("Open Ports:\n")
        print("{:<8} {:<15} {:<20} {}".format("Port", "Service", "Process Name", "Details"))
        print("=" * 70)
        for port, service, process_info in open_ports:
            process_name = process_info.split()[0] if process_info != "No process info available" else "N/A"
            print("{:<8} {:<15} {:<20} {}".format(port, service, process_name, process_info))
    else:
        print("No open ports found.")
