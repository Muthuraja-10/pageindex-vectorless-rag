from app.core.database import get_connection

class KeywordRepository:

    def create_keyword(
            self,
            section_id : int,
            keyword : str
    ):
        
        connection = get_connection()

        try:

             cursor = connection.cursor()

             cursor.execute(
                 """
                    INSERT INTO page_section_keywords
                    (
                      section_id,
                      keyword
                    )
                    VALUES(
                    :1,:2)""",
                    [
                        section_id,
                        keyword
                    ]
             )

             connection.commit()

        finally:
            cursor.close()
            connection.close()

    def search_keywords(
            self,
            keywords: list[str]
    ):
        connection = get_connection()

        try:

            cursor = connection.cursor()

            section_ids =set()

            for keyword in keywords:

                cursor.execute(
                    """
                    SELECT DISTINCT section_id
                    FROM page_section_keywords
                    WHERE LOWER(keyword) LIKE LOWER(:1)
                    """,
                    [f"%{keyword}%"]
                )

                rows = cursor.fetchall()

                for row in rows:
                    section_ids.add(row[0])

            return list(section_ids)
        
        finally:

            cursor.close()
            connection.close()

