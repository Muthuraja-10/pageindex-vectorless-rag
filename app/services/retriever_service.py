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

        # Maximum characters sent to the final LLM.
        # This keeps the request safely below the Groq token limit.
        self.max_context_characters = 24000

    def ask(
        self,
        question: str
    ):

        # --------------------------------
        # Step 1 : Extract Search Keywords
        # --------------------------------

        keywords = self.groq_service.extract_search_keywords(
            question
        )

        # --------------------------------
        # Step 2 : Find Matching Sections
        # --------------------------------

        section_ids = self.keyword_repository.search_keywords(
            keywords
        )

        if not section_ids:
            return {
                "answer": "No relevant information found."
            }

        # --------------------------------
        # Step 3 : Retrieve Relevant Pages
        # --------------------------------

        context_parts = []
        current_length = 0

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

            section_header = f"""
SECTION:
{section["section_title"]}

SUMMARY:
{section["section_summary"]}

"""

            if current_length + len(section_header) > self.max_context_characters:
                break

            context_parts.append(section_header)
            current_length += len(section_header)

            for page_number, page_content in pages:

                page_context = f"""
PAGE {page_number}

{page_content}

---------------------------------------------------
"""

                remaining = (
                    self.max_context_characters
                    - current_length
                )

                if remaining <= 0:
                    break

                if len(page_context) > remaining:
                    page_context = page_context[:remaining]

                context_parts.append(page_context)
                current_length += len(page_context)

                if current_length >= self.max_context_characters:
                    break

            if current_length >= self.max_context_characters:
                break

        context = "".join(context_parts)

        # --------------------------------
        # Step 4 : Generate Answer
        # --------------------------------

        answer = self.groq_service.answer_question(
            context,
            question
        )

        # --------------------------------
        # Step 5 : Return
        # --------------------------------

        return {
            "question": question,
            "answer": answer
        }