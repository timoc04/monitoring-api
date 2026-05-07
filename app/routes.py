from flask import Blueprint, jsonify, request
from .models import Measurement, db

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint to verify that the API is running.

    Returns:
        Response: JSON response with API status.
    """
    return jsonify({"status": "ok"}), 200


@api_bp.route("/measurements", methods=["POST"])
def create_measurement():
    """
    Receives monitoring data and stores it in the database.

    Expected JSON fields:
        hostname (str): Name of the monitored machine.
        ip_address (str): IP address of the monitored machine.
        cpu_usage (float): CPU usage percentage.
        memory_usage (float): Memory usage percentage.

    Returns:
        Response: JSON response with success message or error details.
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    required_fields = [
        "hostname",
        "ip_address",
        "cpu_usage",
        "memory_usage"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    try:
        cpu_usage = float(data["cpu_usage"])
        memory_usage = float(data["memory_usage"])

        measurement = Measurement(
            hostname=data["hostname"],
            ip_address=data["ip_address"],
            cpu_usage=cpu_usage,
            memory_usage=memory_usage
        )

        db.session.add(measurement)
        db.session.commit()

        return jsonify({
            "message": "Measurement stored successfully",
            "measurement": measurement.to_dict()
        }), 201

    except ValueError:
        return jsonify({
            "error": "cpu_usage and memory_usage must be numbers"
        }), 400

    except Exception as error:
        db.session.rollback()

        return jsonify({
            "error": "Database error occurred",
            "details": str(error)
        }), 500


@api_bp.route("/measurements", methods=["GET"])
def get_measurements():
    """
    Retrieves all stored monitoring measurements.

    Returns:
        Response: JSON list containing stored measurements.
    """
    try:
        measurements = Measurement.query.all()

        return jsonify([
            measurement.to_dict()
            for measurement in measurements
        ]), 200

    except Exception as error:
        return jsonify({
            "error": "Could not retrieve measurements",
            "details": str(error)
        }), 500