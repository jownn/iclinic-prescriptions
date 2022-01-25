from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class PrescriptionDb(Base):
    __tablename__ = "prescription"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer)
    physician_id = Column(Integer)
    patient_id = Column(Integer)
    text = Column(String)
    metric_id = Column(Integer)
