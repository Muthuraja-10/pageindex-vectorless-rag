from fastapi import FastAPI
from app.core.database import get_connection
from app.api.document_routes import router as  document_router
from app.api.upload_routes import router as upload_router
from app.api.ask_routes import router as ask_router

app=FastAPI(title="Page Index Retriever API")

@app.get("/")
def home():
    try:
        connection = get_connection()

        connection.close()

        return{
            "message": "Oracle Connected Successfully"
        }
    except Exception as e:
        return{
            "error":str(e)
        }
    

app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(document_router)

