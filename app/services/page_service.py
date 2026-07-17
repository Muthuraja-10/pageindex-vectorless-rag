from app.repositories.page_repository import PageRepository
from app.utils.pdf_reader import extract_pages_from_pdf

class PageService:

    def __init__(self):
        self.page_repository = PageRepository()

    def process_document_pages(
        self,
        document_id : int,
        pdf_path : str
    ):
        pages = extract_pages_from_pdf(
            pdf_path
        ) 

        print(f"Extracted Pages: {len(pages)}")
        
        for page in pages:

            self.page_repository.create_page(
                document_id=document_id,
                page_number=page["page_number"],
                page_content=page["page_content"]
            )
            