import requests
import csv
import time
import os

def convert_bytes(byte_size):
    """Converts bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_size < 1024.0:
            break
        byte_size /= 1024.0
    return f"{byte_size:.2f} {unit}"

def get_glances_data(server, port):
    """Fetches storage data from a Glances API."""
    url = f"http://{server}:{port}/api/3/fs"
    try:
        response = requests.get(url, timeout=5)  # Added timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Timeout error: Unable to reach {server}")
    except requests.exceptions.ConnectionError:
        print(f"Connection error: {server} is unreachable.")
    except requests.RequestException as e:
        print(f"Error accessing Glances API on {server}: {e}")
    return None

def display_drive_info(pool_name, drives):
    """Displays storage info for selected drives and calculates totals."""
    if not drives:
        print(f"No drives available for {pool_name}.")
        return 0, 0, 0

    total_size = total_used = total_free = 0

    print(f"\nSelected Drives Pool for {pool_name}:")
    for drive in drives:
        total_size += drive['size']
        total_used += drive['used']
        total_free += drive['free']

        print(f"Device: {drive['device_name']} - Mount Point: {drive['mnt_point']} - "
              f"Total Size: {convert_bytes(drive['size'])} - Used: {convert_bytes(drive['used'])} - "
              f"Free: {convert_bytes(drive['free'])} - Percent: {drive['percent']}%")

    print(f"\nTotal Pool Size for {pool_name}: {convert_bytes(total_size)} - "
          f"Total Pool Used: {convert_bytes(total_used)} - "
          f"Total Pool Free: {convert_bytes(total_free)}")

    return total_size, total_used, total_free

def write_to_csv(filename, data):
    """Writes storage data to CSV, ensuring headers exist."""
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Total Size", "Total Used", "Total Free"])
        writer.writerow(data)

if __name__ == "__main__":
    hosts = []
    while True:
        host = input("Enter the IP address or hostname of the remote Glances server (or 'done' to finish): ").strip()
        if host.lower() == 'done':
            break
        hosts.append(host)

    port = input("Enter the port of the remote glances server (default is 61208): ").strip() or "61208"
    refresh_interval = input("Enter the refresh interval in seconds (default: 300): ").strip()
    refresh_interval = int(refresh_interval) if refresh_interval.isdigit() else 300

    csv_filename = 'storage_data.csv'

    selected_drives = []

    # Fetch and select drives
    for host in hosts:
        glances_data = get_glances_data(host, port)

        if glances_data:
            print(f"\nAvailable drives for {host}:")
            for i, drive in enumerate(glances_data, start=1):
                print(f"{i}. {drive['device_name']} - {drive['mnt_point']}")

            while True:
                selected_indices = input(f"\nEnter the indices of the drives to include in the pool for Pool Party (comma-separated): ").strip()
                try:
                    selected_indices = [int(index.strip()) - 1 for index in selected_indices.split(',')]
                    if all(0 <= i < len(glances_data) for i in selected_indices):
                        selected_drives.extend([glances_data[i] for i in selected_indices])
                        break
                    else:
                        print("Invalid indices. Please enter numbers from the list above.")
                except ValueError:
                    print("Invalid input. Please enter valid numbers separated by commas.")

    # Main monitoring loop
    while True:
        total_pool_size = total_pool_used = total_pool_free = 0

        for host in hosts:
            glances_data = get_glances_data(host, port)  # Fetch fresh data for selected drives
            if glances_data:
                drives_to_monitor = [drive for drive in glances_data if drive['device_name'] in {d['device_name'] for d in selected_drives}]
                size, used, free = display_drive_info("Pool Party", drives_to_monitor)
                
                total_pool_size += size
                total_pool_used += used
                total_pool_free += free

        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        data_to_write = [current_time, convert_bytes(total_pool_size), convert_bytes(total_pool_used), convert_bytes(total_pool_free)]

        write_to_csv(csv_filename, data_to_write)

        # Sleep for the user-defined refresh interval
        time.sleep(refresh_interval)
