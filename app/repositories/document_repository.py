from app.core.database import get_connection


class DocumentRepository:

    def create_document(self, file_name: str,file_path : str):

        connection = get_connection()

        try:

            cursor = connection.cursor()
            
            document_id = cursor.var(int)

            cursor.execute(
                """
                INSERT INTO page_documents(file_name,file_path)
                VALUES(:1,:2)
                RETURNING document_id INTO:3
                """,
                [file_name,file_path, document_id]
            )

            connection.commit()

            return document_id.getvalue()[0]

        finally:

            cursor.close()
            connection.close()
            