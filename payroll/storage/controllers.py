from fastapi import APIRouter, File, HTTPException, UploadFile

from payroll.storage import services as storage_services
from payroll.storage.schema import FileData

storage_router = APIRouter()


@storage_router.post("/upload", response_model=FileData)
async def upload(file: UploadFile = File(...)):
    if (
        file.content_type
        != "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        raise HTTPException(
            status_code=400, detail="Invalid file format. Only DOCX files are accepted."
        )

    # Read the file content as binary
    file_content = await file.read()

    # Pass the binary content to your storage service
    result = storage_services.upload_file_to_minio(
        file_content, file.filename, file.content_type
    )

    return result
