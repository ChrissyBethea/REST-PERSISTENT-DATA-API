
from sqlalchemy import Column, Integer, String, Float
from database import Base


class ClinicalData(Base):
    __tablename__ = "clinical_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)
    treatment = Column(String, nullable=False)

    # Three additional patient data columns
    blood_type = Column(String, nullable=False)
    allergies = Column(String, nullable=False)
    emergency_contact = Column(String, nullable=False)
