from fastapi import APIRouter,UploadFile,File
from app.services.document_service import DocumentService
import os
from app.services.page_service import PageService
from app.services.section_service import SectionService


router = APIRouter()

document_service = DocumentService()
page_service = PageService()
section_service = SectionService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    uploads_folder = "app/uploads"

    os.makedirs(
        uploads_folder,
        exist_ok=True)
    
    file_path = os.path.join(
        uploads_folder,
        file.filename)

    with open(file_path,"wb") as buffer:

        content = await file.read()
        buffer.write(content)


    document_id = document_service.create_document(
        file.filename,
        file_path
    )

    page_service.process_document_pages(
        document_id,
        file_path
    )

    section_result = section_service.process_sections(
    document_id
    )

    return{
        "document_id":document_id,
        "file_name":file.filename,
        "file_path":file_path,
        "message":"Document Uploaded",
        "section_result": section_result
    }
