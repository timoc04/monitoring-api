"""
monitoring_application.py
version 6.0

Collects basic system metrics and sends them to the Monitoring API.
It can also retrieve stored monitoring data from the API.
"""

import os
import time

import psutil
import requests
from dotenv import load_dotenv


load_dotenv()

API_URL = os.getenv("API_URL")


def validate_api_url():
    """
    Checks if the API_URL environment variable is configured.

    Returns:
        bool: True if API_URL exists, otherwise False.
    """
    if not API_URL:
        print("Error: API_URL is not configured. Check your .env file.")
        return False

    return True


def collect_system_metrics():
    """
    Collects hostname, IP address, CPU usage and memory usage.

    Returns:
        dict: Collected monitoring data.
    """
    hostname = input("Enter hostname: ")
    ip_address = input("Enter IP address: ")

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "cpu_usage": float(cpu_usage),
        "memory_usage": float(memory_usage)
    }


def send_data():
    """
    Sends collected monitoring data to the configured API endpoint.

    Returns:
        None
    """
    if not validate_api_url():
        return

    data = collect_system_metrics()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.post(API_URL, json=data, timeout=10)
        response.raise_for_status()

        print("\nData collected and sent to API:")
        print(
            f"Timestamp: {timestamp} | "
            f"Hostname: {data['hostname']} | "
            f"IP: {data['ip_address']} | "
            f"CPU: {data['cpu_usage']:.1f}% | "
            f"Memory: {data['memory_usage']:.1f}%"
        )
        print(f"API response: {response.status_code} - {response.text}")

    except requests.exceptions.Timeout:
        print("Error: The request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
        print(f"API response: {response.text}")

    except requests.exceptions.RequestException as error:
        print(f"Unexpected request error occurred: {error}")


def show_data():
    """
    Retrieves and displays stored monitoring data from the API.

    Returns:
        None
    """
    if not validate_api_url():
        return

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        rows = response.json()

        if not rows:
            print("No data found in API yet.")
            return

        print("\nStored monitoring data from API:")

        for row in rows:
            print(
                f"{row.get('id')}: "
                f"{row.get('hostname')} | "
                f"{row.get('ip_address')} | "
                f"CPU: {row.get('cpu_usage'):.1f}% | "
                f"Memory: {row.get('memory_usage'):.1f}% | "
                f"{row.get('timestamp')}"
            )

    except requests.exceptions.Timeout:
        print("Error: The request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
        print(f"API response: {response.text}")

    except ValueError:
        print("Error: API response is not valid JSON.")

    except requests.exceptions.RequestException as error:
        print(f"Unexpected request error occurred: {error}")


def main():
    """
    Displays the menu and runs the selected function.

    Returns:
        None
    """
    print("1. Collect and send data")
    print("2. Show stored data")

    choice = input("Choose an option (1/2): ")

    if choice == "1":
        send_data()
    elif choice == "2":
        show_data()
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()