import json
from groq import Groq
from app.core.config import settings


class GroqService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def generate_response(self, prompt: str):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        return response.choices[0].message.content

    def detect_sections(
        self,
        document_content: str
    ):

        prompt = f"""
You are an expert document analyzer.

Your task is to analyze the following document and identify all major sections.

For every section return:

- section_title
- section_summary
- keywords
- start_page
- end_page

Rules:

1. Return ONLY a valid JSON array.
2. Do NOT explain anything.
3. Do NOT add markdown.
4. Do NOT use ```json.
5. Do NOT write "Here is the result".
6. Do NOT write any text before or after the JSON.
7. Keywords must be an array of strings.
8. start_page and end_page must be integers.
9. section_summary must be one or two concise sentences.

Return exactly like this:

[
    {{
        "section_title": "Introduction",
        "section_summary": "Overview of the document.",
        "keywords": [
            "FastAPI",
            "Python",
            "Backend"
        ],
        "start_page": 1,
        "end_page": 3
    }}
]

Document:

{document_content}
"""

        return self.generate_response(prompt)
    
    def extract_search_keywords(
            self,
            question : str
    ):
        prompt = f"""
         
            You are a search query analyzer. 

            Extract the most important search Keywords from the user's question. 

            Rules:
            -Return ONLY a valid JSON array.
            -Maximum 5 keywords. 
            -No explanation. 
            -No markdown. 

            Example 1:

            Question:
            What is CAPEX? 

            Output:
            ["CAPEX"]

            Example 2:

            Question:
            What is Cloud Governance. 

            Output:
            ["Cloud Governance"]

            Example 3:

            Question:
            How does cloud pricing works?

            Output:
            ["Cloud Pricing"]

            Question:

            {question}
            """
        
        response = self.generate_response(prompt)
        return json.loads(response)
    

    def answer_question(
                self,
                context: str,
                question: str
        ):

            prompt = f"""
        You are an AI assistant.

        Answer the question ONLY from the given document context.

        If the answer is not available in the context, reply exactly:

        "I couldn't find that information in the uploaded document."

        -----------------------
        DOCUMENT CONTEXT
        -----------------------

        {context}

        -----------------------
        QUESTION
        -----------------------

        {question}

        -----------------------
        ANSWER
        -----------------------
        """

            return self.generate_response(prompt)
    
    