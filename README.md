# Pool Party

## This project is in its most basic form. There is not a clear and concise alpha as of today 12/26/23 documentation will be provided as soon as the project progresses. 

## This readme is for where the project is in it current unfinished state. 

## Overview

**Pool Party** is a Python script designed to make managing and monitoring disk drives on remote servers a breeze. It interacts with a Glances server, retrieving information about available drives, and allows you to create a pool of selected drives. Whether you're a system administrator or just curious about your server's disk usage, Pool Party provides a straightforward way to visualize and analyze drive metrics.

## Features

- **Remote Monitoring**: Connect to your Glances server remotely to gather real-time information about available drives.

- **Drive Pool Creation**: Select specific drives to include in a pool for consolidated monitoring and analysis.

- **User-Friendly Interface**: A simple and intuitive command-line interface guides you through the process of configuring and monitoring drive pools.

- **Detailed Drive Information**: View details such as device names, mount points, total size, used space, free space, and percentage usage for each drive.

## Requirements

- Python 3.x
- The `requests` library (install using `pip install requests`)

## Usage

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/pool-party.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd pool-party
    ```

3. **Run the Script:**

    ```bash
    python pool_party.py
    ```

4. **Follow On-Screen Prompts:**

    Enter the IP address or hostname of the remote Glances server, select the drives to include in the pool, and view a summary of the total pool size, used space, and free space.

## Configuration

- The default port for the Glances server is set to `61208`. If your Glances server uses a different port, you can specify it during script execution.
