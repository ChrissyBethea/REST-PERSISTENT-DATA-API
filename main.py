
import json
import os

from flask import Flask, jsonify, request
from pydantic import ValidationError

from database import Base, SessionLocal, engine
from models import ClinicalData
from schemas import ClinicalDataCreate

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

os.makedirs("data", exist_ok=True)
JSONL_FILE = "data/clinical_data.jsonl"


@app.route("/clinical/", methods=["POST"])
def create_clinical_record():
    try:
        validated = ClinicalDataCreate.model_validate(request.get_json())
    except (ValidationError, ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400

    db = SessionLocal()

    try:
        record = ClinicalData(**validated.model_dump())
        db.add(record)
        db.commit()
        db.refresh(record)

        result = {
            "id": record.id,
            **validated.model_dump()
        }

        with open(JSONL_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(result) + "\n")

        return jsonify(result), 201

    except Exception as error:
        db.rollback()
        return jsonify({"error": str(error)}), 500

    finally:
        db.close()


@app.route("/clinical/", methods=["GET"])
def get_clinical_records():
    db = SessionLocal()

    try:
        records = db.query(ClinicalData).all()

        results = [
            {
                "id": record.id,
                "patient_name": record.patient_name,
                "age": record.age,
                "diagnosis": record.diagnosis,
                "treatment": record.treatment,
                "blood_type": record.blood_type,
                "allergies": record.allergies,
                "emergency_contact": record.emergency_contact
            }
            for record in records
        ]

        return jsonify(results), 200

    finally:
        db.close()


if __name__ == "__main__":
    app.run(port=5003, debug=True)
