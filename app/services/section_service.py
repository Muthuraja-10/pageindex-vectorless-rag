import json

from app.repositories.page_repository import PageRepository
from app.repositories.section_repository import SectionRepository
from app.repositories.keyword_repository import KeywordRepository
from app.services.groq_service import GroqService


class SectionService:

    def __init__(self):

        self.page_repository = PageRepository()
        self.section_repository = SectionRepository()
        self.keyword_repository = KeywordRepository()
        self.groq_service = GroqService()

    def process_sections(
        self,
        document_id: int
    ):

        # Step 1 : Load all pages from Oracle
        pages = self.page_repository.get_pages_by_document_id(
            document_id
        )

        

        if not pages:
            return {
                "message": "No pages found for this document."
            }

       

        # Step 2 : Combine all pages into one document
        document_content = ""

        for page_number, page_content in pages:

            document_content += f"""

PAGE {page_number}

{page_content}

-------------------------------------------------------

"""

        print("=" * 80)
        print("DOCUMENT CONTENT (FIRST 1000 CHARACTERS)")
        print("=" * 80)
        print(document_content[:1000])
        print("=" * 80)

        # Step 3 : Send document to Groq
        groq_response = self.groq_service.detect_sections(
            document_content
        )

        sections = json.loads(groq_response)

        total_sections = 0
        total_keywords = 0

        for section in sections:

            section_id = self.section_repository.create_section(

                document_id=document_id,
                section_title=section["section_title"],
                section_summary=section["section_summary"],
                start_page=section["start_page"],
                end_page=section["end_page"]
            )

            total_sections += 1

            for keyword in section["keywords"]:

                self.keyword_repository.create_keyword(
                    section_id,
                    keyword
                )

                total_keywords += 1

        return {

            "message":"Section Indexed Successfully",
            "section_created":total_sections,
            "keywords_created":total_keywords
        }
    
    def get_sections(
       self,
       document_id: int
     ):

         return self.section_repository.get_sections_by_document(
        document_id
    )