from pydantic import BaseModel

class UploadResponse(BaseModel):

    document_id : int
    file_name : str
    message : str

    