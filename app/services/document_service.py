from app.repositories.document_repository import DocumentRepository


class DocumentService:

    def __init__(self):

       self.document_repository = DocumentRepository()

    def create_document(self, file_name: str,file_path : str):

        document_id =  self.document_repository.create_document(
            file_name,file_path
        )
        return document_id
