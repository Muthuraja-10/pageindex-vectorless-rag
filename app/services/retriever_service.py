from app.services.groq_service import GroqService
from app.repositories.keyword_repository import KeywordRepository
from app.repositories.section_repository import SectionRepository
from app.repositories.page_repository import PageRepository


class RetrieverService:

    def __init__(self):

        self.groq_service = GroqService()
        self.keyword_repository = KeywordRepository()
        self.section_repository = SectionRepository()
        self.page_repository = PageRepository()

    def ask(
        self,
        question: str
    ):

       

        keywords = self.groq_service.extract_search_keywords(
            question
        )


        section_ids = self.keyword_repository.search_keywords(
            keywords
        )
  

        if not section_ids:

            return {
                "answer": "No relevant information found."
            }


        context = ""

        for section_id in section_ids:

            section = self.section_repository.get_section(
                section_id
            )

            if section is None:
                continue

            pages = self.page_repository.get_pages_between(
                section["document_id"],
                section["start_page"],
                section["end_page"]
            )

            context += f"""

SECTION :
{section['section_title']}

SUMMARY :
{section['section_summary']}

"""

            for page_number, page_content in pages:

                context += f"""

PAGE {page_number}

{page_content}

---------------------------------------------------

"""


        answer = self.groq_service.answer_question(
            context,
            question
        )

        return {
            "question": question,
           # "keywords": keywords,
            #"matched_sections": section_ids,
            "answer": answer
        }