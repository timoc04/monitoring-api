from flask import Blueprint, request, jsonify
from .models import db, Measurement

api_bp = Blueprint("api", __name__)

@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/measurements", methods=["POST"])
def create_measurement():
    data = request.get_json(force=True)

    m = Measurement(
        hostname=data.get("hostname"),
        ip_address=data.get("ip_address"),
        cpu_usage=data.get("cpu_usage"),
        memory_usage=data.get("memory_usage"),
    )

    db.session.add(m)
    db.session.commit()

    return jsonify({"message": "measurement stored", "id": m.id}), 201


@api_bp.route("/measurements", methods=["GET"])
def list_measurements():
    measurements = Measurement.query.order_by(Measurement.timestamp.desc()).limit(50)
    return jsonify([m.to_dict() for m in measurements]), 200
