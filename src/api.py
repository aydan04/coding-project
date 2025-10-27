import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict

from . import scanner, database

router = APIRouter()

# Ensure the 'uploads' directory exists
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@router.post("/scan-file/")
async def scan_file(file: UploadFile = File(...)):
    """
    Accepts a file for scanning, saves it, performs a scan,
    stores the report, and returns the report ID.
    """
    try:
        file_location = os.path.join(UPLOADS_DIR, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        # Generate a report for the uploaded file
        report = scanner.generate_report(file_location)

        # Generate a unique report ID and save the report
        report_id = str(uuid.uuid4())
        database.save_report(report_id, report)

        return {"filename": file.filename, "report_id": report_id}
    except Exception as e:
        # In a real application, log the error properly
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/reports/{report_id}")
async def get_report(report_id: str) -> Dict:
    """
    Retrieves an analysis report by its ID.
    """
    report = database.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report
