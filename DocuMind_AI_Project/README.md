# DocuMind AI — Intelligent Document Question Answering System

## Academic scope
This prototype implements a deterministic document-QA pipeline using explicit structured records, an inverted keyword index, and hand-written inference rules. It does **not** use NLP libraries/pipelines, RAG, embeddings, vector databases, LLM APIs, or generative models.

## Important notice
The included handbook is fictional sample data for coursework. It is **not** an official MS Ramaiah University of Applied Sciences publication or statement of actual university policy.

## Project structure
- `app.py` — Streamlit web application
- `data/Sample_Student_Handbook.docx` — editable source handbook
- `data/Sample_Student_Handbook.pdf` — PDF source handbook
- `data/knowledge_base.json` — structured seed knowledge base
- `tests/evaluation_questions.csv` — sample evaluation set
- `reports/` — report files

## Run in VS Code
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Create a virtual environment:
   - Windows: `py -m venv .venv`
   - Activate: `.venv\\Scripts\\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `streamlit run app.py`
6. Open the local URL shown in the terminal.

## How it works
1. The user selects the sample handbook or uploads a PDF/DOCX.
2. Text extraction uses PyMuPDF for PDF and python-docx for DOCX.
3. The parser extracts lines in the explicit format `FACT: id | label | value | ALIASES: alias1; alias2`.
4. Each fact is represented as a record in a structured knowledge base.
5. An inverted index maps terms to fact IDs.
6. The question is tokenized using basic regular-expression splitting (not a linguistic NLP pipeline).
7. Matching facts are ranked by shared-token count.
8. Explicit rules handle attendance eligibility, scholarship threshold checks, and library fine calculation.
9. The answer includes the method and supporting knowledge records.

## Custom document format
For reliable extraction, include one record per line:
`FACT: attendance.minimum | Minimum attendance requirement | 75% | ALIASES: attendance; minimum attendance; eligibility`

## Limitations
- Keyword overlap can miss paraphrases and can return a wrong top match when wording is ambiguous.
- The custom parser requires explicit FACT records; it is not a universal semantic document-understanding engine.
- Rules are manually authored for the sample handbook and do not automatically infer arbitrary new rules.
- Scanned/image-only PDFs require OCR, which is not included.
- The app is an educational prototype, not an official policy-advice tool.

## Suggested demo questions
- What is the minimum attendance required?
- A student has 68% attendance. Is the student eligible for the exam?
- What are the library operating hours?
- What is the overdue fine for 3 books for 4 days?
- What SGPA is required for the sample merit scholarship?
