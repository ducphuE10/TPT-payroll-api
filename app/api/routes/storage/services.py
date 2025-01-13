import os
from typing import Optional
import uuid
import base64
from io import BytesIO
from app.storage.schema import FileData

BASE_DIR = "/var/www/uploads"


# Ensure the base directory exists (create it if it doesn't)
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)


def upload_file_to_local_server(
    file_content: bytes, filename: str, content_type: str
) -> FileData:
    try:
        # Generate a unique file ID and define the full path to store the file
        file_id = str(uuid.uuid4())
        file_path = os.path.join(BASE_DIR, f"{file_id}_{filename}")

        if isinstance(file_content, str):
            raise ValueError("file_content should be a bytes-like object, not a string")

        # Save the file to the local file system
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Encode the file content in base64 (optional, for returning it)
        file_content_base64 = base64.b64encode(file_content).decode("utf-8")

        return FileData(
            filename=filename,
            content_type=content_type,
            file=file_content_base64,
            message="File upload successful.",
            path=file_path,
        )
    except Exception as e:
        return {
            "status": False,
            "error": str(e),
            "message": "File upload failed due to an internal error.",
        }


def read_file_from_local_server(file_path: str) -> Optional[BytesIO]:
    try:
        # Read the file from the local file system
        if not os.path.exists(file_path):
            raise FileNotFoundError("File does not exist.")

        file_in_memory = BytesIO()

        with open(file_path, "rb") as f:
            file_in_memory.write(f.read())

        file_in_memory.seek(0)  # Reset the stream's position
        return file_in_memory

    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None
