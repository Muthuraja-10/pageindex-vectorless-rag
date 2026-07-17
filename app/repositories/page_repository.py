from app.core.database import get_connection


class PageRepository:

    def create_page(
        self,
        document_id: int,
        page_number: int,
        page_content: str
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO page_pages
                (
                    document_id,
                    page_number,
                    page_content
                )
                VALUES
                (
                    :1,
                    :2,
                    :3
                )
                """,
                [
                    document_id,
                    page_number,
                    page_content
                ]
            )

            connection.commit()

        finally:

            cursor.close()
            connection.close()

    def get_pages_by_document_id(
        self,
        document_id: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    page_number,
                    page_content
                FROM page_pages
                WHERE document_id = :1
                ORDER BY page_number
                """,
                [document_id]
            )

            rows = cursor.fetchall()

            pages = []

            for page_number, page_content in rows:

                pages.append(
                    (
                        page_number,
                        page_content.read()
                    )
                )

            return pages

        finally:

            cursor.close()
            connection.close()

    def get_pages_between(
        self,
        document_id: int,
        start_page: int,
        end_page: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    page_number,
                    page_content
                FROM page_pages
                WHERE document_id = :1
                  AND page_number BETWEEN :2 AND :3
                ORDER BY page_number
                """,
                [
                    document_id,
                    start_page,
                    end_page
                ]
            )

            rows = cursor.fetchall()

            pages = []

            for page_number, page_content in rows:

                if hasattr(page_content, "read"):
                    page_content = page_content.read()

                pages.append(
                    (
                        page_number,
                        page_content
                    )
                )

            return pages

        finally:

            cursor.close()
            connection.close()