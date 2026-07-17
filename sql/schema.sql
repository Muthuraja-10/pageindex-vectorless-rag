CREATE TABLE page_documents (
    document_id NUMBER GENERATED ALWAYS AS IDENTITY,
    file_name VARCHAR2(255),
    file_path VARCHAR2(500),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(document_id)
);

CREATE TABLE page_pages (
    page_id NUMBER GENERATED ALWAYS AS IDENTITY,
    document_id NUMBER,
    page_number NUMBER,
    page_content CLOB,
    PRIMARY KEY(page_id),
    FOREIGN KEY(document_id)
        REFERENCES page_documents(document_id)
);

CREATE TABLE page_sections (
    section_id NUMBER GENERATED ALWAYS AS IDENTITY,
    document_id NUMBER,
    section_title VARCHAR2(500),
    section_summary CLOB,
    start_page NUMBER,
    end_page NUMBER,
    PRIMARY KEY(section_id),
    FOREIGN KEY(document_id)
        REFERENCES page_documents(document_id)
);

CREATE TABLE page_section_keywords (
    keyword_id NUMBER GENERATED ALWAYS AS IDENTITY,
    section_id NUMBER,
    keyword VARCHAR2(200),
    PRIMARY KEY(keyword_id),
    FOREIGN KEY(section_id)
        REFERENCES page_sections(section_id)
);