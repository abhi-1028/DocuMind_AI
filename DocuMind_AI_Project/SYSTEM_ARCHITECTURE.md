# System Architecture

```text
PDF/DOCX Input
     |
     v
Text Extraction (PyMuPDF / python-docx)
     |
     v
FACT Record Parser
     |
     v
Structured Knowledge Base
     |
     +------> Inverted Index
                    |
User Question ------+
     |
     v
Rule Dispatcher (R1, R2, R3)
     |
     +---- rule matched ----> Inference result
     |
     +---- no rule ---------> Keyword-ranked fact retrieval
                                  |
                                  v
                         Answer + evidence
                                  |
                                  v
                           Streamlit UI
```

## Why this approach?
It directly satisfies the assignment's allowed techniques: knowledge representation, search, rules, inference and reasoning. It avoids NLP and RAG.
