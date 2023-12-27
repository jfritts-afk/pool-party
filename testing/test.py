import requests
import socket
import ipaddress

def is_valid_ip(ip):
    """Check if the given string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def convert_bytes(byte_size):
    """Convert bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_size < 1024.0:
            break
        byte_size /= 1024.0
    return f"{byte_size:.2f} {unit}"

def get_glances_data(server, port):
    """Fetch Glances data from the specified server and port."""
    url = f"http://{server}:{port}/api/3/fs"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()
        return data
    except requests.ConnectionError as ce:
        print(f"Error connecting to Glances API on {server}: {ce}")
    except requests.HTTPError as he:
        print(f"HTTP error from Glances API on {server}: {he}")
    except requests.RequestException as e:
        print(f"Error accessing Glances API on {server}: {e}")
    return None

def display_drive_info(host, drives):
    """Display drive information for a given host."""
    if not drives:
        print(f"No drives available for {host}.")
        return

    total_size = total_used = total_free = 0

    print(f"\nSelected Drives Pool for {host}:")
    for drive in drives:
        total_size += drive['size']
        total_used += drive['used']
        total_free += drive['free']

        print(f"Device: {drive['device_name']} - Mount Point: {drive['mnt_point']} - "
              f"Total Size: {convert_bytes(drive['size'])} - Used: {convert_bytes(drive['used'])} - "
              f"Free: {convert_bytes(drive['free'])} - Percent: {drive['percent']}%")

    print(f"\nTotal Pool Size for {host}: {convert_bytes(total_size)} - Total Pool Used: {convert_bytes(total_used)} - "
          f"Total Pool Free: {convert_bytes(total_free)}")

    return total_size, total_used, total_free

if __name__ == "__main__":
    hosts = []
    while True:
        host = input("Enter the IP address or hostname of the remote glances server (or 'done' to finish): ")
        if host.lower() == 'done':
            break
        elif is_valid_ip(host) or socket.gethostbyname(host) != host:
            hosts.append(host)
        else:
            print("Invalid IP address or hostname. Please enter a valid IP address or hostname.")

    port = input("Enter the port of the remote glances server (default is 61208): ") or "61208"

    total_pool_size = total_pool_used = total_pool_free = 0

    for host in hosts:
        glances_data = get_glances_data(host, port)

        if glances_data:
            drives = glances_data
            print("\nAvailable drives:")
            for i, drive in enumerate(drives, start=1):
                print(f"{i}. {drive['device_name']} - {drive['mnt_point']}")

            selected_indices = input(f"\nEnter the indices of the drives to include in the pool for {host} (comma-separated): ")
            selected_indices = [int(index.strip()) - 1 for index in selected_indices.split(',')]

            selected_drives = [drives[index] for index in selected_indices]
            size, used, free = display_drive_info(host, selected_drives)

            total_pool_size += size
            total_pool_used += used
            total_pool_free += free

    print("\nSummary:")
    print(f"Total Pool Size: {convert_bytes(total_pool_size)} - Total Pool Used: {convert_bytes(total_pool_used)} - "
          f"Total Pool Free: {convert_bytes(total_pool_free)}")
