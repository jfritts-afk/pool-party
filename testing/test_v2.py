import requests
import csv
import time

def convert_bytes(byte_size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_size < 1024.0:
            break
        byte_size /= 1024.0
    return f"{byte_size:.2f} {unit}"

def get_glances_data(server, port):
    url = f"http://{server}:{port}/api/3/fs"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error accessing Glances API on {server}: {e}")
        return None

def display_drive_info(pool_name, drives):
    if not drives:
        print(f"No drives available for {pool_name}.")
        return

    total_size = total_used = total_free = 0

    print(f"\nSelected Drives Pool for {pool_name}:")
    for drive in drives:
        total_size += drive['size']
        total_used += drive['used']
        total_free += drive['free']

        print(f"Device: {drive['device_name']} - Mount Point: {drive['mnt_point']} - "
              f"Total Size: {convert_bytes(drive['size'])} - Used: {convert_bytes(drive['used'])} - "
              f"Free: {convert_bytes(drive['free'])} - Percent: {drive['percent']}%")

    print(f"\nTotal Pool Size for {pool_name}: {convert_bytes(total_size)} - Total Pool Used: {convert_bytes(total_used)} - "
          f"Total Pool Free: {convert_bytes(total_free)}")

    return total_size, total_used, total_free

def write_to_csv(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

if __name__ == "__main__":
    hosts = []
    while True:
        host = input("Enter the IP address or hostname of the remote glances server (or 'done' to finish): ")
        if host.lower() == 'done':
            break
        hosts.append(host)

    port = input("Enter the port of the remote glances server (default is 61208): ") or "61208"

    refresh_interval = int(input("Enter the refresh interval in seconds (e.g., 60 for 1 minute): ") or 300)

    csv_filename = 'storage_data.csv'

    drives = []

    for host in hosts:
        glances_data = get_glances_data(host, port)

        if glances_data:
            print(f"\nAvailable drives for {host}:")
            for i, drive in enumerate(glances_data, start=1):
                print(f"{i}. {drive['device_name']} - {drive['mnt_point']}")

            selected_indices = input(f"\nEnter the indices of the drives to include in the pool for Pool Party (comma-separated): ")
            selected_indices = [int(index.strip()) - 1 for index in selected_indices.split(',')]

            selected_drives = [glances_data[index] for index in selected_indices]
            drives.extend(selected_drives)

    while True:
        total_pool_size = total_pool_used = total_pool_free = 0

        for host in hosts:
            size, used, free = display_drive_info("Pool Party", drives)

            total_pool_size += size
            total_pool_used += used
            total_pool_free += free

        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        data_to_write = [current_time, convert_bytes(total_pool_size), convert_bytes(total_pool_used),
                         convert_bytes(total_pool_free)]

        write_to_csv(csv_filename, data_to_write)

        # Sleep for the user-defined refresh interval
        time.sleep(refresh_interval)
