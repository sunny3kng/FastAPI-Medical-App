from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define the models using Pydantic
class Patient(BaseModel):
    id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    is_available: Optional[bool] = True

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: str

# In-memory data structures to store patients, doctors, and appointments
patients = []
doctors = []
appointments = []

# CRUD endpoints for Patients
@app.post("/patients/")
def create_patient(patient: Patient):
    patients.append(patient)
    return patient

@app.get("/patients/")
def get_patients():
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: Patient):
    for index, existing_patient in enumerate(patients):
        if existing_patient.id == patient_id:
            patients[index] = patient
            return {"message": "Patient updated successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for index, patient in enumerate(patients):
        if patient.id == patient_id:
            del patients[index]
            return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")

# CRUD endpoints for Doctors
@app.post("/doctors/")
def create_doctor(doctor: Doctor):
    doctors.append(doctor)
    return doctor

@app.get("/doctors/")
def get_doctors():
    return doctors

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for doctor in doctors:
        if doctor.id == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor: Doctor):
    for index, existing_doctor in enumerate(doctors):
        if existing_doctor.id == doctor_id:
            doctors[index] = doctor
            return {"message": "Doctor updated successfully"}
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    for index, doctor in enumerate(doctors):
        if doctor.id == doctor_id:
            del doctors[index]
            return {"message": "Doctor deleted successfully"}
    raise HTTPException(status_code=404, detail="Doctor not found")

# Create an appointment
@app.post("/appointments/")
def create_appointment(appointment: Appointment):
    for doctor in doctors:
        if doctor.is_available:
            doctor.is_available = False
            appointments.append(appointment)
            return appointment
    raise HTTPException(status_code=400, detail="No available doctors")

# Complete an appointment
@app.put("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment.id == appointment_id:
            for doctor in doctors:
                if doctor.id == appointment.doctor_id:
                    doctor.is_available = True
                    appointments.remove(appointment)
                    return {"message": "Appointment completed successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")

# Cancel an appointment
@app.put("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment.id == appointment_id:
            for doctor in doctors:
                if doctor.id == appointment.doctor_id:
                    doctor.is_available = True
                    appointments.remove(appointment)
                    return {"message": "Appointment canceled successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")

# Set availability status for doctors
@app.put("/doctors/{doctor_id}/set_availability")
def set_doctor_availability(doctor_id: int, is_available: bool):
    for doctor in doctors:
        if doctor.id == doctor_id:
            doctor.is_available = is_available
            return {"message": f"Availability status for doctor {doctor_id} set to {is_available}"}
    raise HTTPException(status_code=404, detail="Doctor not found")
