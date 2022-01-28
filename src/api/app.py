import uvicorn
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.config import config
from src.model.database import PrescriptionDb
from src.model.exceptions import RequestException, get_exception
from src.model.requests import PrescriptionRequest, MetricRequest

import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db

from src.model.responses import PrescriptionResponse, ClinicResponse, PatientResponse, PhysicianResponse, MetricResponse
from src.service.api.iclinic import ClinicService, PatientService, PhysicianService, MetricService
from src.utils import load_env

load_env()

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

base_url = config['BaseUrl']
clinic_service_config = config['ClinicService']
patient_service_config = config['PatientService']
physician_service_config = config['PhysicianService']
metric_service_config = config['MetricService']

clinic_service = ClinicService(base_url + clinic_service_config['method'],
                               auth_token=clinic_service_config['token'])
physician_service = PhysicianService(base_url + physician_service_config['method'],
                                     auth_token=physician_service_config['token'])
patient_service = PatientService(base_url + patient_service_config['method'],
                                 auth_token=patient_service_config['token'])
metric_service = MetricService(base_url + metric_service_config['method'],
                               auth_token=metric_service_config['token'])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    exception: RequestException = get_exception(service=1, status_code=status_code)
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"error": {"message": exception.message, "code": exception.code}})
    )


@app.exception_handler(RequestException)
async def request_exception_handler(request: Request, exc: RequestException):
    db.session.rollback()
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"error": {"message": exc.message, "code": exc.code}}),
    )


@app.post("/prescriptions", response_model=PrescriptionResponse)
async def create_prescription(prescription: PrescriptionRequest):
    db_prescription = PrescriptionDb()
    db_prescription.clinic_id = prescription.clinic.id
    db_prescription.physician_id = prescription.physician.id
    db_prescription.patient_id = prescription.patient.id
    db_prescription.text = prescription.text
    db.session.add(db_prescription)
    db.session.flush()

    clinic = clinic_service.get(prescription.clinic.id)
    physician = physician_service.get(prescription.physician.id)
    patient = patient_service.get(prescription.patient.id)

    metric = MetricRequest(
        physician_id=physician["id"],
        physician_name=physician["name"],
        physician_crm=physician["crm"],
        patient_id=patient["id"],
        patient_name=patient["name"],
        patient_email=patient["email"],
        patient_phone=patient["phone"],
        prescription_id=db_prescription.id
    )
    if clinic is not None:
        metric.clinic_id = clinic["id"]
        metric.clinic_name = clinic["name"]

    metric_response = metric_service.post(metric)

    prescription_response = PrescriptionResponse(
        clinic=ClinicResponse(id=prescription.clinic.id),
        patient=PatientResponse(id=prescription.patient.id),
        physician=PhysicianResponse(id=prescription.physician.id),
        text=prescription.text,
        metric=MetricResponse(id=metric_response["id"])
    )
    return prescription_response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
