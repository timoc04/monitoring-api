"""
monitor_application1.py
version 4.0

Description:
This script collects simple system metrics (CPU and Memory)
and saves them to a local SQLite database through an API. 
It also allows users to view stored data from the database.

Has two modes:
1. Collect new data
2. Show stored data
"""
import time
import socket
import psutil
import requests

API_URL = "http://127.0.0.1:5000/api/measurements"

def collect_data():
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

    response = requests.post(API_URL, json=data)

    print("\nData collected and sent to API:")
    print(f"Timestamp: {timestamp} | Hostname: {hostname} | IP: {ip} | CPU: {cpu:.1f}% | Memory: {memory:.1f}%")
    print(f"API response: {response.status_code} - {response.text}")

def show_data():
    response = requests.get(API_URL)

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