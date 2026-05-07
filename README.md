# Monitoring API - The Knowledge Hub

This repository contains the Python Flask Monitoring API and monitoring script for Case Study 2.

## Project goal
The goal of this project is to collect monitoring data from systems and send it to a central API. The API stores the data in an Azure SQL Database.

This supports:
- REQ-S2P2-04: Centralized Monitoring Data Store
- REQ-S2P2-05: Monitoring Data Access Interface
- REQ-S2P2-06: Enhanced Monitoring Application

## Technologies
- Python
- Flask
- Azure Container Apps
- Azure SQL Database
- GitHub Actions
- Docker
- python-dotenv

## API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Checks if the API is running |
| `/api/measurements` | POST | Sends monitoring data to the API |
| `/api/measurements` | GET | Retrieves stored monitoring data |

## Environment variables

Create a `.env` file based on `.env.example`.

Required variables:

```env
API_URL=
DB_SERVER=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_DRIVER=ODBC Driver 18 for SQL Server