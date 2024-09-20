import logging

from fastapi import UploadFile

from payroll.storage.schema import FileData
from payroll.storage.services import upload_file_to_local_server

log = logging.getLogger(__name__)


def upload_fileStorage(*, db_session, file: UploadFile) -> FileData:
    """Uploads a file to the storage."""
    try:
        file_data = FileData(
            file=file.file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )
        file_data = upload_file_to_local_server(file_data)
        return file_data
    except Exception as e:
        log.error(f"Error uploading file: {e}")
        return FileData(status=False, error=str(e))
