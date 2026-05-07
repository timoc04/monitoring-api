from flask import Blueprint, jsonify, request

from .models import Measurement, db

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/measurements", methods=["POST"])
def create_measurement():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    required_fields = [
        "hostname",
        "ip_address",
        "cpu_usage",
        "memory_usage"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        measurement = Measurement(
            hostname=data["hostname"],
            ip_address=data["ip_address"],
            cpu_usage=float(data["cpu_usage"]),
            memory_usage=float(data["memory_usage"]),
        )

        db.session.add(measurement)
        db.session.commit()

        return jsonify({
            "message": "measurement stored",
            "id": measurement.id
        }), 201

    except ValueError:
        return jsonify({
            "error": "cpu_usage and memory_usage must be numbers"
        }), 400

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500