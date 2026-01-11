# Multi-Modal Prompt Refinement System

## 🚀 Project Overview
A full-stack AI application that standardizes vague user inputs (text, sketches, PDFs) into structured technical requirements using Google Gemini 2.0.

**Tech Stack:**
* **Frontend:** React (Vite) + CSS Modules
* **Backend:** Python FastAPI
* **AI Engine:** Google Gemini (Multimodal capabilities)

---

## 🧠 Thought Process & Problem Solving

### 1. The Core Challenge: Ambiguity
Users rarely know exactly what they want. A client might say "I want an Uber for tractors" or upload a messy napkin sketch. Raw LLMs struggle with this without guidance.
**My Solution:** I designed a "Strict Schema" approach. Instead of letting the AI chat back, I force it to output a specific JSON structure (`core_intent`, `specifications`, `deliverables`). This ensures downstream agents (like Devin or AutoGPT) can use the output programmatically.

### 2. Architecture Decisions
* **Why FastAPI?** I chose FastAPI over Flask/Django because of its native support for Pydantic data validation and asynchronous processing (crucial for waiting on AI responses without blocking the server).
* **Why Gemini?** I evaluated OpenAI GPT-4o and Claude 3. I selected **Gemini 2.0/1.5** because it has native "Multimodal" support. It doesn't need a separate OCR library (like Tesseract) to read PDFs or Images; it "sees" them natively, reducing system complexity and latency.

### 3. Handling "Multi-Modal" Complexity
The biggest technical hurdle was unifying different input streams.
* **Strategy:** I implemented a `Multipart/Form-Data` pipeline.
* **Logic:** The backend checks the MIME type.
    * `image/*`: Passed directly to the Vision model.
    * `application/pdf`: parsed via `pypdf` to extract raw text context.
    * `text/plain`: Used as system instructions.
This allows the user to upload a *sketch* of a login screen and *write* "Make it blue," and the system combines both contexts.

---

## 🛡️ Validation & Error Handling
* **JSON Enforcement:** The system explicitly instructs the LLM to strip Markdown formatting (` ```json `) to prevent parsing errors.
* **Empty Input Handling:** The Frontend validates that either text or a file exists before sending a request to save API tokens.

## 🔮 Limitations & Future Improvements
If I had more time, I would implement:
1.  **Streaming Responses:** Currently, the user waits 2-3 seconds. I would use Server-Sent Events (SSE) to stream the text as it generates.
2.  **Human-in-the-Loop:** A "Edit" feature so users can correct the AI's assumptions before finalizing the prompt.
3.  **Prompt Versioning:** Saving previous refinements to a database (MongoDB) to track changes.

---

## 🏃‍♂️ How to Run Locally

1. **Clone the Repo**

2. **Backend Setup**
   ```Bash
   cd ai-prompt-refiner
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
    ```Bash
    cd client
    npm install
    npm run dev
    ```
    ---
### By Mufaddal Virpurwala
