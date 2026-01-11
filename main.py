import os
import json
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf  # CHANGED: Using the modern library
from io import BytesIO

# 1. Load the API Key from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Warning: GEMINI_API_KEY not found in .env file.")

# 2. Configure Google Gemini AI
# (Ignore the "FutureWarning" in your terminal, this library works fine for now)
if api_key:
    genai.configure(api_key=api_key)

# 3. Initialize the App
app = FastAPI()

# 4. Allow your Frontend (React) to talk to this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HELPER FUNCTION: Read PDF Files ---
def extract_text_from_pdf(file_bytes) -> str:
    try:
        # CHANGED: Updated to use pypdf syntax
        reader = pypdf.PdfReader(BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# --- THE MAIN ENDPOINT ---
@app.post("/refine")
async def refine_prompt(
    text_input: Optional[str] = Form(None),
    files: List[UploadFile] = File(None)
):
    print("Received request...") 

    # A. Define the strict JSON structure we want
    system_instruction = """
    You are an expert Technical Business Analyst.
    Your task: Analyze the provided text, images, or documents.
    Output ONLY a valid JSON object matching this structure:
    {
      "meta_info": { "confidence_score": "High/Medium/Low" },
      "core_intent": { 
          "summary": "1-sentence summary", 
          "target_audience": "Who is this for?", 
          "primary_goal": "Main problem solved" 
      },
      "specifications": { 
          "functional_requirements": ["list", "of", "requirements"], 
          "technical_constraints": ["list", "of", "constraints"], 
          "design_preferences": ["style", "colors", "etc"] 
      },
      "deliverables": ["list", "of", "outputs"]
    }
    If info is missing, infer it reasonably or mark as "Not Specified".
    Do NOT use Markdown formatting (like ```json). Just return the raw JSON.
    """

    content_parts = [system_instruction]

    # B. Add user's text if they sent any
    if text_input:
        print(f"Processing text input: {text_input[:50]}...")
        content_parts.append(f"User Description: {text_input}")

    # C. Add user's files if they sent any
    if files:
        for file in files:
            print(f"Processing file: {file.filename}")
            content = await file.read()
            
            if file.content_type.startswith("image/"):
                content_parts.append({
                    "mime_type": file.content_type,
                    "data": content
                })
            elif file.content_type == "application/pdf":
                pdf_text = extract_text_from_pdf(content)
                content_parts.append(f"Document Content from {file.filename}: {pdf_text}")

    # D. Send to AI
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(content_parts)
        
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        response_json = json.loads(clean_text)
        
        return response_json

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))