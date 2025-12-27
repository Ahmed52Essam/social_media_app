import logging
import tempfile

import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, status

from social_media_app.libs.b2 import b2_upload_file

logger = logging.getLogger(__name__)

router = APIRouter()

# Life cycle of upload endpoint
# Client -> server (tempfile) -> B2 -> delete temp file

# 1- Client split up the file into chuncks 1 MB
# 2- Client sends up chuncks 1 at a time
# 3- Client sends the  last chunck
# 4- fastapi puts all the chucncks into 1 temp file
# 5- it uploads the file to B2 and then deletes the temp file

CHUNCK_SIZE = 1024 * 1024


@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile):
    try:
        with tempfile.NamedTemporaryFile() as temp_file:
            file_name = temp_file.name
            logger.debug(f"Saving uploaded file temporarily to {file_name}")
            async with aiofiles.open(file_name, "wb") as f:
                while chunck := await file.read(CHUNCK_SIZE):
                    await f.write(chunck)
            file_url = b2_upload_file(local_file=file_name, file_name=file.filename)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )
    return {"detail": f"Sucessfully uploaded {file.filename}", "file_url": file_url}
