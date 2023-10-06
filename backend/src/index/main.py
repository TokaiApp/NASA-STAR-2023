from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ai import AI
from storage import BlobStorage

origins = [
    "*"
]

app = FastAPI(title="Tokai API Endpoints", 
              #docs_url=None,  # Disable docs (Swagger UI)
              #redoc_url=None,  # Disable redoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)

# Create a homepage route
@app.get("/")
def index():
    return {"server ok": True}
@app.post("/api/sidekick/pdf")
async def upload_pdf_sidekick(request: Request, user_email: str = Form(...), 
                              file_name: str = Form(...),
                              file: UploadFile = File(...)):
    """
    Upload a PDF file to Azure Blob Storage
    """
    file_content = await file.read()
    storage = BlobStorage()
    result = storage.upload_blob(file=file_content, file_name=file_name, user_email=user_email)
    
    if result:
        return {"result": True}
    else:
        return {"result": False}
    
@app.post("/api/sidekick/chat")
async def sidekick_chat(request: Request, user_request: str = Form(...)):
    """
    Chat with Tokai
    """
    # Get the text content in the user request
    ai = AI()
    result = ai.sidekick_chat(user_request=user_request)
    
    return {"result": result}