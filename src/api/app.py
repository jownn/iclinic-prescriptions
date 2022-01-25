import uvicorn
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.model.database import PrescriptionDb
from src.model.exceptions import RequestException
from src.model.requests import PrescriptionDto

import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from dotenv import load_dotenv

BASE_DIR = '/app'
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"error": {"message": "malformed request", "code": 1}})
    )


@app.exception_handler(RequestException)
async def request_exception_handler(request: Request, exc: RequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"error": {"message": exc.message, "code": exc.code}}),
    )


@app.get("/prescriptions/{prescription_id}")
async def create_prescription(prescription_id: int):
    if prescription_id == 1:
        raise HTTPException(status_code=404, detail="prescription not found")
    return 2


@app.post("/prescriptions", response_model=PrescriptionDto)
async def create_prescription(prescription: PrescriptionDto):
    db_prescription = PrescriptionDb()
    db_prescription.clinic_id = prescription.clinic.id
    db_prescription.physician_id = prescription.physician.id
    db_prescription.patient_id = prescription.patient.id
    db_prescription.text = prescription.text
    db.session.add(db_prescription)

    if db_prescription.clinic_id == 1:
        db.session.rollback()
        raise RequestException(status_code=404, message="prescription not found", code=3)

    db.session.commit()
    return prescription


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
