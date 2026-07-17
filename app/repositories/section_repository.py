from app.core.database import get_connection


class SectionRepository:

    def create_section(
        self,
        document_id: int,
        section_title: str,
        section_summary: str,
        start_page: int,
        end_page: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            section_id = cursor.var(int)

            cursor.execute(
                """
                INSERT INTO page_sections
                (
                    document_id,
                    section_title,
                    section_summary,
                    start_page,
                    end_page
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    :5
                )
                RETURNING section_id INTO :6
                """,
                [
                    document_id,
                    section_title,
                    section_summary,
                    start_page,
                    end_page,
                    section_id
                ]
            )

            connection.commit()

            return section_id.getvalue()[0]

        finally:

            cursor.close()
            connection.close()

    def get_section(
        self,
        section_id: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    document_id,
                    section_title,
                    section_summary,
                    start_page,
                    end_page
                FROM page_sections
                WHERE section_id = :1
                """,
                [section_id]
            )

            row = cursor.fetchone()

            if row is None:
                return None

            section_summary = row[2]

            if hasattr(section_summary, "read"):
                section_summary = section_summary.read()

            return {
                "document_id": row[0],
                "section_title": row[1],
                "section_summary": section_summary,
                "start_page": row[3],
                "end_page": row[4]
            }

        finally:

            cursor.close()
            connection.close()

    def get_sections_by_document(
        self,
        document_id: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    section_id,
                    section_title,
                    start_page,
                    end_page
                FROM page_sections
                WHERE document_id = :1
                ORDER BY section_id
                """,
                [document_id]
            )

            rows = cursor.fetchall()

            return [
                {
                    "section_id": row[0],
                    "section_title": row[1],
                    "start_page": row[2],
                    "end_page": row[3]
                }
                for row in rows
            ]

        finally:

            cursor.close()
            connection.close()