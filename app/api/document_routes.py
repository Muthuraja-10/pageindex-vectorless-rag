from fastapi import APIRouter
from app.services.document_service import DocumentService
from app.repositories.section_repository import SectionRepository
from app.repositories.page_repository import PageRepository
from app.services.section_service import SectionService
from app.services.groq_service import GroqService
from app.repositories.keyword_repository import KeywordRepository

router = APIRouter()

document_service = DocumentService()
section_repository = SectionRepository()
page_repository = PageRepository()
section_service = SectionService()
groq_service = GroqService()
keyword_repository = KeywordRepository()





@router.get("/documents/{document_id}/sections")
def get_sections(document_id: int):

    return section_service.get_sections(document_id)


@router.get("/section-info/{section_id}")
def section_info(section_id: int):

    return section_repository.get_section(section_id)

@router.get("/pages/{document_id}/pages")
def get_pages(document_id : int):
    pages = page_repository.get_pages_by_document_id(
        document_id
    )

    return{
        "total_pages":len(pages)
    }


@router.get("/pages-between/{document_id}/{start}/{end}")
def pages_between(
    document_id: int,
    start: int,
    end: int
):
    return page_repository.get_pages_between(
        document_id,
        start,
        end
    )