import streamlit as st
import json
import re
import io
import html
from pathlib import Path

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN SYSTEM — OBSIDIAN / EMERALD / WARM IVORY
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --bg: #111512;
    --surface: #191f1b;
    --surface-2: #202923;
    --surface-3: #28332c;
    --border: #303d34;
    --text: #f1f0e8;
    --muted: #a6b0a7;
    --green: #70c69a;
    --green-dark: #1c7658;
    --ivory: #e9e3d4;
    --copper: #c58b62;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse at 12% 0%, rgba(58, 105, 75, .17), transparent 34%),
        radial-gradient(ellipse at 90% 8%, rgba(197, 139, 98, .07), transparent 26%),
        var(--bg);
    color: var(--text);
}
[data-testid="stHeader"] {
    background: rgba(17, 21, 18, .88);
}
.block-container {
    max-width: 1380px;
    padding-top: 1.7rem;
    padding-bottom: 2.5rem;
}
h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -.035em;
}
p, label, .stMarkdown, .stCaption {
    color: var(--text);
}
small, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #151b17;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.4rem;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    font-size: 1.05rem;
    letter-spacing: -.02em;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: var(--surface);
    border: 1px dashed #53675a;
    border-radius: 14px;
    padding: 10px;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    padding: 30px 34px;
    border-radius: 22px;
    background: linear-gradient(115deg, #202b23 0%, #26392d 58%, #31483a 100%);
    border: 1px solid #405747;
    box-shadow: 0 18px 48px rgba(0,0,0,.18);
    margin-bottom: 24px;
}
.hero:after {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    border: 1px solid rgba(170,220,185,.13);
    border-radius: 50%;
    right: -65px;
    top: -115px;
    box-shadow: 0 0 0 28px rgba(170,220,185,.035),
                0 0 0 58px rgba(170,220,185,.025);
}
.eyebrow {
    color: #a9d7b8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .17em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.hero h1 {
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 800;
    margin: 0 0 7px 0;
    line-height: 1.1;
}
.hero p {
    color: #d2ded4;
    margin: 0;
    font-size: 14px;
}
.hero-tag {
    display: inline-block;
    margin-top: 18px;
    padding: 7px 11px;
    border: 1px solid rgba(180,220,190,.25);
    border-radius: 30px;
    color: #d6eadb;
    background: rgba(12,30,19,.28);
    font-size: 11px;
    letter-spacing: .04em;
}

/* Section headings and surfaces */
.section-kicker {
    color: var(--green);
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: 10px;
    font-weight: 700;
    margin-bottom: 5px;
}
.section-title {
    font-family: 'Manrope', sans-serif;
    color: var(--text);
    font-size: 1.35rem;
    font-weight: 750;
    margin: 0 0 4px 0;
}
.section-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 16px;
}
.surface {
    background: linear-gradient(145deg, #1b231e, #18201b);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 19px 21px;
    margin-bottom: 14px;
}
.document-strip {
    display: flex;
    align-items: center;
    gap: 13px;
    background: #1b251e;
    border: 1px solid #35483a;
    border-radius: 15px;
    padding: 14px 17px;
    margin: 10px 0 20px 0;
}
.doc-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #2a4935;
    font-size: 20px;
}
.doc-name {
    font-weight: 700;
    color: var(--ivory);
    font-size: 14px;
}
.doc-meta {
    color: var(--muted);
    font-size: 11px;
    margin-top: 2px;
}
.status-pill {
    margin-left: auto;
    border-radius: 30px;
    padding: 6px 10px;
    color: #a9e2bd;
    background: rgba(57,139,88,.16);
    border: 1px solid rgba(112,198,154,.25);
    font-size: 11px;
    font-weight: 700;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #202a23, #19211c);
    border: 1px solid #35443a;
    border-radius: 16px;
    padding: 17px 19px;
    box-shadow: 0 8px 22px rgba(0,0,0,.10);
}
[data-testid="stMetricLabel"] {
    color: #aab7ac !important;
    font-size: 12px !important;
}
[data-testid="stMetricValue"] {
    color: #f0eee4 !important;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
}

/* Inputs */
.stTextInput input {
    background: #151d18 !important;
    color: var(--text) !important;
    border: 1px solid #435348 !important;
    border-radius: 12px !important;
    min-height: 48px;
}
.stTextInput input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 1px var(--green) !important;
}
.stTextInput label, .stCheckbox label, .stFileUploader label {
    color: var(--ivory) !important;
    font-weight: 600 !important;
}
.stButton > button {
    border-radius: 11px;
    min-height: 43px;
    border: 1px solid #52745c;
    background: #286747;
    color: #f5fff7;
    font-weight: 700;
    transition: all .18s ease;
}
.stButton > button:hover {
    background: #347e56;
    border-color: #78c996;
    color: white;
    transform: translateY(-1px);
}
.stButton > button[kind="secondary"] {
    background: #202a23;
    border: 1px solid #39483e;
    color: #dce5dc;
}
.stButton > button[kind="secondary"]:hover {
    background: #2a382e;
    border-color: #6a9476;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    color: #b7c1b8;
    background: transparent;
    border-radius: 9px 9px 0 0;
    padding: 10px 16px;
}
.stTabs [aria-selected="true"] {
    color: #a9e2bd !important;
    border-bottom: 2px solid var(--green) !important;
}
.stExpander {
    background: #1b241e;
    border: 1px solid var(--border);
    border-radius: 12px;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}
hr {
    border-color: var(--border) !important;
}
.answer-card {
    background: linear-gradient(135deg, #1c3024, #1b2820);
    border: 1px solid #42664c;
    border-left: 4px solid var(--green);
    border-radius: 15px;
    padding: 19px 21px;
    color: #f1f5ed;
    line-height: 1.7;
    margin: 12px 0;
    font-size: 15px;
}
.answer-label {
    color: #9ed8ae;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .15em;
    text-transform: uppercase;
    margin-bottom: 7px;
}
.method-chip {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 20px;
    background: #252f28;
    border: 1px solid #3b4b3f;
    color: #b7c8b9;
    font-size: 11px;
}
.empty-state {
    text-align: center;
    padding: 34px 20px;
    background: #1a231d;
    border: 1px dashed #526454;
    border-radius: 17px;
}
.empty-icon {
    font-size: 30px;
    margin-bottom: 8px;
}
.footer {
    color: #829086;
    font-size: 11px;
    text-align: center;
    letter-spacing: .04em;
    padding: 10px 0 0 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">Knowledge • Search • Reasoning</div>
    <h1>DocuMind AI</h1>
    <p>An intelligent document question-answering workspace.</p>
    <span class="hero-tag">DOCUMENT INTELLIGENCE WORKSPACE</span>
</div>
""", unsafe_allow_html=True)

NOTICE = (
    "Teaching prototype only. The included handbook contains fictional "
    "sample policies and is NOT an official MS Ramaiah University policy document."
)

# ============================================================
# DOCUMENT PROCESSING
# ============================================================

def extract_text(uploaded):
    name = uploaded.name.lower()
    data = uploaded.getvalue()

    if name.endswith(".pdf"):
        import fitz
        pdf = fitz.open(stream=data, filetype="pdf")
        return "\n".join(page.get_text("text") for page in pdf)

    if name.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(data))
        chunks = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                chunks.append(" | ".join(c.text for c in row.cells))
        return "\n".join(chunks)

    raise ValueError("Please upload a PDF or DOCX file.")


def parse_knowledge(text):
    facts = []
    pattern = re.compile(
        r"FACT:\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*ALIASES:\s*(.*?)(?=\s*FACT:|\Z)",
        re.I | re.S
    )

    for m in pattern.finditer(text):
        facts.append({
            "id": m.group(1).strip(),
            "label": m.group(2).strip(),
            "value": re.sub(r"\s+", " ", m.group(3)).strip(),
            "aliases": [
                x.strip().lower()
                for x in re.sub(r"\s+", " ", m.group(4)).split(";")
                if x.strip()
            ]
        })

    unique = {}
    for fact in facts:
        unique[fact["id"]] = fact
    return list(unique.values())


# ============================================================
# RULE-BASED LANGUAGE MATCHING
# ============================================================

# Manually curated vocabulary mappings; no NLP model is used.
SYNONYMS = {
    "attendance": [
        "attendance", "attend", "attending", "presence",
        "class presence", "class attendance", "classes attended"
    ],
    "minimum": [
        "minimum", "least", "required", "requirement",
        "necessary", "needed", "threshold"
    ],
    "exam": ["exam", "exams", "examination", "examinations", "test", "tests"],
    "eligibility": [
        "eligibility", "eligible", "qualified",
        "qualification", "allowed", "permitted"
    ],
    "hours": [
        "hours", "timings", "timing", "operating",
        "opening", "schedule", "working hours"
    ],
    "fine": [
        "fine", "penalty", "charge", "charges",
        "fee", "overdue", "late fee"
    ],
    "library": ["library", "books", "book"],
    "scholarship": [
        "scholarship", "merit award", "financial aid", "student award"
    ],
    "sgpa": [
        "sgpa", "grade point", "semester grade",
        "academic score", "grade"
    ],
    "disciplinary": [
        "disciplinary", "discipline", "misconduct",
        "punishment", "penalty"
    ],
    "deadline": ["deadline", "last date", "due date", "submission date"]
}

WORD_TO_CANONICAL = {}
for canonical, variations in SYNONYMS.items():
    for phrase in variations:
        for token in re.findall(r"[a-z0-9]+", phrase.lower()):
            WORD_TO_CANONICAL[token] = canonical

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "of", "for", "to", "in",
    "on", "how", "many", "much", "do", "does", "i", "we", "you",
    "can", "could", "would", "should", "my", "me", "it", "and", "or",
    "be", "have", "has", "there", "this", "that", "from", "with",
    "about", "tell", "please", "explain", "give", "find"
}


def normalize_tokens(text):
    raw = re.findall(r"[a-z0-9]+", text.lower())
    result = []
    for token in raw:
        if token in STOPWORDS:
            continue
        canonical = WORD_TO_CANONICAL.get(token, token)
        if canonical not in result:
            result.append(canonical)
    return set(result)


# ============================================================
# KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve(question, facts):
    query_tokens = normalize_tokens(question)
    scores = {}

    for fact in facts:
        fact_id = fact["id"]
        label_tokens = normalize_tokens(fact["label"])
        alias_tokens = set()
        for alias in fact.get("aliases", []):
            alias_tokens.update(normalize_tokens(alias))
        id_tokens = normalize_tokens(fact_id.replace(".", " "))
        searchable = label_tokens | alias_tokens | id_tokens

        score = (
            len(query_tokens & label_tokens) * 3
            + len(query_tokens & alias_tokens) * 3
            + len(query_tokens & id_tokens)
        )
        coverage = (
            len(query_tokens & searchable) / len(query_tokens)
            if query_tokens else 0
        )
        score += coverage * 2

        scores[fact_id] = {
            "score": score,
            "coverage": coverage,
            "fact": fact
        }

    return sorted(scores.values(), key=lambda x: x["score"], reverse=True)


# ============================================================
# REASONING RULES
# ============================================================

def answer_question(question, facts):
    q = question.lower().strip()
    byid = {f["id"]: f for f in facts}
    ranked = retrieve(question, facts)
    evidence = [
        item["fact"] for item in ranked[:5] if item["score"] > 0
    ]
    tokens = normalize_tokens(question)

    # Rule R1: Attendance eligibility
    attendance_intent = "attendance" in tokens
    exam_intent = bool({"exam", "eligibility"} & tokens)
    attendance_match = re.search(r"(\d{1,3})\s*%", q)

    if attendance_match and attendance_intent and (
        exam_intent or "attendance.minimum" in byid
    ):
        minimum = byid.get("attendance.minimum", {}).get("value", "75%")
        number = re.search(r"\d+", minimum)

        if number:
            pct = int(attendance_match.group(1))
            threshold = int(number.group())
            if pct >= threshold:
                result = (
                    f"{pct}% attendance meets the sample minimum "
                    f"requirement of {threshold}%. Other examination "
                    f"requirements may still apply."
                )
            else:
                result = (
                    f"{pct}% attendance is below the sample minimum "
                    f"requirement of {threshold}%. The attendance "
                    f"condition is not satisfied."
                )
            return result, evidence, "Rule R1: Attendance reasoning"

    # Rule R3: Library fine calculation
    fine_intent = "fine" in tokens
    fine_match = re.search(r"(\d+)\s+books?.{0,40}?(\d+)\s+days?", q)

    if fine_match and fine_intent:
        books, days = map(int, fine_match.groups())
        rate = byid.get("library.fine", {}).get(
            "value", "₹2 per book per day"
        )
        rate_match = re.search(r"\d+", rate)
        if rate_match:
            rate_num = int(rate_match.group())
            return (
                f"{books} book(s) × {days} day(s) × ₹{rate_num} "
                f"= ₹{books * days * rate_num}.",
                evidence,
                "Rule R3: Fine calculation"
            )

    # Rule R2: Scholarship reasoning
    scholarship_intent = "scholarship" in tokens
    sgpa_match = re.search(r"\b(?:sgpa\s*)?(\d(?:\.\d+)?)\b", q)

    if scholarship_intent and sgpa_match:
        sgpa = float(sgpa_match.group(1))
        threshold_text = byid.get("scholarship.merit", {}).get(
            "value", "8.5"
        )
        threshold_match = re.search(r"\d+(?:\.\d+)?", threshold_text)

        if threshold_match:
            threshold = float(threshold_match.group())
            if sgpa >= threshold:
                result = (
                    f"An SGPA of {sgpa:.2f} meets the sample minimum "
                    f"of {threshold:.1f}. The sample rule also requires "
                    f"no active disciplinary penalty."
                )
            else:
                result = (
                    f"An SGPA of {sgpa:.2f} is below the sample "
                    f"minimum of {threshold:.1f}."
                )
            return result, evidence, "Rule R2: Scholarship reasoning"

    # General weighted retrieval
    if not ranked or ranked[0]["score"] <= 0:
        return (
            "I couldn't find sufficient matching information in the "
            "uploaded document. Try rephrasing your question.",
            [],
            "No reliable match"
        )

    best = ranked[0]
    second_score = ranked[1]["score"] if len(ranked) > 1 else 0

    if best["coverage"] < 0.34:
        return (
            "I found a possible match, but there isn't enough overlapping "
            "information to answer confidently.",
            evidence,
            "Low confidence"
        )

    if second_score > 0 and best["score"] - second_score < 1:
        return (
            "Your question matches multiple knowledge records. Please add "
            "a little more detail so I can identify the correct one.",
            evidence,
            "Ambiguous match"
        )

    fact = best["fact"]
    return (
        f"{fact['label']}: {fact['value']}",
        [fact],
        "Weighted rule-based retrieval"
    )


# ============================================================
# SIDEBAR WORKSPACE
# ============================================================

with st.sidebar:
    st.markdown("## 📚 DocuMind AI")
    st.caption("DOCUMENT INTELLIGENCE WORKSPACE")
    st.divider()

    st.markdown("### Workspace")
    sample = st.checkbox("Use sample student handbook", value=True)

    uploaded = st.file_uploader(
        "Add a document",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX"
    )

    st.divider()
    st.markdown("### How it works")
    st.caption("01  Document text extraction")
    st.caption("02  Structured knowledge representation")
    st.caption("03  Weighted keyword retrieval")
    st.caption("04  Rule-based inference")

    st.divider()
    st.markdown("### System approach")
    st.caption(
        "Knowledge representation • Curated synonym mapping • "
        "Search • Deterministic reasoning"
    )
    st.caption("No NLP pipeline, RAG, embeddings, vector database or external LLM API.")


# ============================================================
# LOAD DOCUMENT
# ============================================================

try:
    if uploaded is not None:
        source_text = extract_text(uploaded)
        facts = parse_knowledge(source_text)
        source_name = uploaded.name
        source_type = "Uploaded document"
    elif sample:
        BASE_DIR = Path(__file__).resolve().parent
        kb_path = BASE_DIR / "data" / "knowledge_base.json"

        kb = json.loads(
            kb_path.read_text(encoding="utf-8")
        )

        facts = kb["facts"]
        source_name = "Sample Student Handbook"        facts = kb["facts"]
        source_name = "Sample Student Handbook"
        source_type = "Built-in sample knowledge base"
    else:
        facts = []
        source_name = "No document selected"
        source_type = "Waiting for document"
except Exception as e:
    st.error(f"Document processing error: {e}")
    facts = []
    source_name = "Error"
    source_type = "Processing error"

# ============================================================
# DASHBOARD OVERVIEW
# ============================================================

st.markdown('<div class="section-kicker">WORKSPACE OVERVIEW</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Your document at a glance</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">A quick overview of the active document and its knowledge records.</div>',
    unsafe_allow_html=True
)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Document status", "Ready" if facts else "Not loaded")
with m2:
    st.metric("Knowledge records", len(facts))
with m3:
    st.metric("Reasoning engine", "Rule-based AI")

safe_name = html.escape(source_name)
safe_type = html.escape(source_type)
status_text = "READY TO QUERY" if facts else "NOT CONNECTED"
st.markdown(f"""
<div class="document-strip">
    <div class="doc-icon">📄</div>
    <div>
        <div class="doc-name">{safe_name}</div>
        <div class="doc-meta">{safe_type}</div>
    </div>
    <div class="status-pill">{status_text}</div>
</div>
""", unsafe_allow_html=True)

st.info(NOTICE, icon="ℹ️")

# ============================================================
# MAIN APPLICATION
# ============================================================

if facts:
    tab1, tab2 = st.tabs(["💬  Ask your document", "🧠  Knowledge base"])

    with tab1:
        st.markdown('<div class="section-kicker">DOCUMENT ASSISTANT</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">What would you like to know?</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Ask a question about the active document. DocuMind will retrieve relevant records and apply available reasoning rules.</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True):
            question = st.text_input(
                "Enter your question",
                placeholder="e.g. What attendance is needed to be eligible for exams?",
                key="question"
            )
            ask = st.button("⌕  Find answer", type="primary", use_container_width=True)

        if ask:
            if question.strip():
                answer, evidence, method = answer_question(question, facts)
                st.markdown('<div class="answer-label">DOCUMIND RESPONSE</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="answer-card">{html.escape(answer)}</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<span class="method-chip">Reasoning method · {html.escape(method)}</span>',
                    unsafe_allow_html=True
                )

                if evidence:
                    st.markdown("#### Supporting knowledge")
                    for fact in evidence:
                        with st.expander(f"📌  {fact['label']}"):
                            st.write(fact["value"])
                            st.caption(f"Fact ID: {fact['id']}")
            else:
                st.warning("Enter a question before searching.")

        st.markdown("---")
        st.markdown("#### Suggested questions")
        st.caption("Select a question to use it as a starting point.")

        examples = [
            "What is the minimum attendance required?",
            "How many classes must I attend to sit for exams?",
            "A student has 68% attendance. Can they take the exam?",
            "What are the library opening timings?",
            "Calculate the late fee for 3 books for 4 days.",
            "What SGPA is needed for a merit scholarship?"
        ]

        def use_example(example_text):
            st.session_state["question"] = example_text

        for start in range(0, len(examples), 2):
            cols = st.columns(2)
            for col, example in zip(cols, examples[start:start + 2]):
                with col:
                    st.button(
                        example,
                        key=f"example_{start}_{examples.index(example)}",
                        use_container_width=True,
                        on_click=use_example,
                        args=(example,)
                    )

    with tab2:
        st.markdown('<div class="section-kicker">STRUCTURED INFORMATION</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Constructed knowledge base</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">The facts and aliases available to the retrieval and reasoning engine.</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            [
                {
                    "Fact ID": f["id"],
                    "Concept": f["label"],
                    "Stored value": f["value"],
                    "Aliases": ", ".join(f.get("aliases", []))
                }
                for f in facts
            ],
            use_container_width=True,
            hide_index=True
        )
        st.caption(f"{len(facts)} structured knowledge record(s) loaded.")

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>No knowledge base loaded</h3>
        <p style="color:#a6b0a7;">Choose the sample handbook or upload a supported PDF/DOCX document containing structured FACT records.</p>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "Ordinary PDF/DOCX text is not automatically converted into knowledge "
        "records. This prototype requires explicit FACT records for reliable extraction."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    '<div class="footer">DOCUMIND AI  ·  ACADEMIC PROTOTYPE  ·  KNOWLEDGE REPRESENTATION / SEARCH / RULES / REASONING</div>',
    unsafe_allow_html=True
)
