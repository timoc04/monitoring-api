"""
monitoring_application.py
version 5.0

Description:
This script collects simple system metrics and sends them to the Azure API.
It also allows users to view stored data from the API.
"""

import os
import time

import psutil
import requests
from dotenv import load_dotenv


load_dotenv()
API_URL = os.getenv("API_URL")


def collect_data():
    if not API_URL:
        print("API_URL is not configured. Check your .env file.")
        return

    hostname = input("Enter hostname: ")
    ip = input("Enter IP address: ")

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "hostname": hostname,
        "ip_address": ip,
        "cpu_usage": float(cpu),
        "memory_usage": float(memory)
    }

    try:
        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )

        print("\nData collected and sent to API:")
        print(
            f"Timestamp: {timestamp} | Hostname: {hostname} | IP: {ip} | "
            f"CPU: {cpu:.1f}% | Memory: {memory:.1f}%"
        )
        print(f"API response: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as error:
        print(f"Failed to send data to API: {error}")


def show_data():
    if not API_URL:
        print("API_URL is not configured. Check your .env file.")
        return

    try:
        response = requests.get(
            API_URL,
            timeout=10
        )

        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code} - {response.text}")
            return

        rows = response.json()

        if not rows:
            print("No data found in API yet.")
            return

        print("\nStored monitoring data (from API)")
        for row in rows:
            print(
                f"{row['id']}: "
                f"{row['hostname']} | "
                f"{row['ip_address']} | "
                f"CPU: {row['cpu_usage']:.1f}% | "
                f"Memory: {row['memory_usage']:.1f}% | "
                f"{row['timestamp']}"
            )

    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch data from API: {error}")


def main():
    print("1. Collect and send data")
    print("2. Show stored data")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        collect_data()
    elif choice == "2":
        show_data()
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
    