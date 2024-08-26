from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from pydantic import BaseModel
from llama3_model import LLaMA3Model
import aiofiles
import re

app = FastAPI()

# Load the LLaMA 3 model
model = LLaMA3Model(model_name="meta-llama/Llama-2-7b-hf")

# Bad language filter (simple example)
BAD_WORDS = ["badword1", "badword2"]  # Replace with actual bad words

class Query(BaseModel):
    text: str

@app.post("/generate/")
async def generate(query: Query):
    # Filter bad language
    for word in BAD_WORDS:
        if re.search(rf'\b{word}\b', query.text, re.IGNORECASE):
            raise HTTPException(status_code=400, detail="Inappropriate language detected.")
    
    # Generate response using LLaMA 3
    response = model.generate_response(query.text)
    return {"response": response}

@app.post("/upload-document/")
async def upload_document(file: UploadFile = File(...)):
    # Save the uploaded file
    async with aiofiles.open(f"./uploads/{file.filename}", 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Example of document processing (just returning the first 100 characters for demonstration)
    text_content = content.decode('utf-8')
    summary = model.summarize_text(text_content)
    return {"summary": summary}

# Simple 2FA (for demonstration)
users = {"user@example.com": "123456"}  # Example user database

@app.post("/2fa/")
async def two_factor_auth(email: str = Form(...), code: str = Form(...)):
    if email in users and users[email] == code:
        return {"message": "2FA successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or code.")
