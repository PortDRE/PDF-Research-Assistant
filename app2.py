# ============================================================
# PDF RESEARCH ASSISTANT — SELF-SETTING-UP VERSION
#
# First run:
#     py app.py
#
# Later runs:
#     py app.py
#
# Do not run "streamlit run app.py" manually.
# This script creates a Python 3.12 environment, installs all
# dependencies, downloads the models, and starts Streamlit.
# ============================================================

import os
import sys
import subprocess
from pathlib import Path


# ------------------------------------------------------------
# AUTOMATIC SETUP
# ------------------------------------------------------------

PROJECT_DIRECTORY = Path(__file__).resolve().parent
VENV_DIRECTORY = PROJECT_DIRECTORY / ".venv312"
SETUP_MARKER = VENV_DIRECTORY / ".setup_complete"
SCRIPT_PATH = Path(__file__).resolve()

REQUIRED_PACKAGES = [
    "streamlit",
    "pymupdf",
    "faiss-cpu",
    "numpy",
    "torch",
    "sentence-transformers",
    "transformers",
    "sentencepiece",
    "safetensors",
]


def get_venv_python():
    """Return the virtual-environment Python executable."""
    if os.name == "nt":
        return VENV_DIRECTORY / "Scripts" / "python.exe"

    return VENV_DIRECTORY / "bin" / "python"


def find_python_312():
    """Find Python 3.12 installed on Windows or another OS."""
    commands = []

    if os.name == "nt":
        commands.extend([
            ["py", "-3.12"],
            ["python3.12"],
        ])
    else:
        commands.extend([
            ["python3.12"],
            ["python"],
        ])

    for command in commands:
        try:
            result = subprocess.run(
                command + [
                    "-c",
                    "import sys; print(sys.executable) "
                    "if sys.version_info[:2] == (3, 12) else exit(1)"
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            executable = result.stdout.strip()

            if executable:
                return command

        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    return None


def create_virtual_environment():
    """Create a Python 3.12 virtual environment."""
    python_command = find_python_312()

    if python_command is None:
        print("\nERROR: Python 3.12 was not found.")
        print("Install Python 3.12 and then run:")
        print("    py app.py")
        print("\nDownload Python 3.12 from:")
        print("https://www.python.org/downloads/")
        input("\nPress Enter to close...")
        sys.exit(1)

    print("\nCreating the Python 3.12 environment...")

    subprocess.run(
        python_command + ["-m", "venv", str(VENV_DIRECTORY)],
        check=True,
    )


def install_dependencies(venv_python):
    """Install all packages required by the application."""
    print("\nUpdating pip, setuptools and wheel...")

    subprocess.run(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "setuptools",
            "wheel",
        ],
        check=True,
    )

    print("\nInstalling application dependencies...")
    print("This can take several minutes on the first run.\n")

    subprocess.run(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            *REQUIRED_PACKAGES,
        ],
        check=True,
    )

    SETUP_MARKER.touch()


def start_inside_streamlit(venv_python):
    """Restart this file using Streamlit inside Python 3.12."""
    environment = os.environ.copy()
    environment["PDF_ASSISTANT_STREAMLIT_STARTED"] = "1"

    print("\nStarting the PDF Research Assistant...")
    print("The application will open in your browser.\n")

    subprocess.run(
        [
            str(venv_python),
            "-m",
            "streamlit",
            "run",
            str(SCRIPT_PATH),
        ],
        env=environment,
        check=True,
    )

    sys.exit(0)


def bootstrap_application():
    """Prepare the environment before importing third-party libraries."""

    # When Streamlit has restarted this file inside the virtual
    # environment, continue to the actual application.
    if os.environ.get("PDF_ASSISTANT_STREAMLIT_STARTED") == "1":
        if sys.version_info[:2] != (3, 12):
            raise RuntimeError(
                "The application must run using Python 3.12."
            )
        return

    try:
        venv_python = get_venv_python()

        if not venv_python.exists():
            create_virtual_environment()

        venv_python = get_venv_python()

        if not SETUP_MARKER.exists():
            install_dependencies(venv_python)

        start_inside_streamlit(venv_python)

    except subprocess.CalledProcessError as error:
        print("\nAutomatic setup failed.")
        print(f"Command returned error code: {error.returncode}")
        print("\nCheck the internet connection and run again:")
        print("    py app.py")
        input("\nPress Enter to close...")
        sys.exit(1)


bootstrap_application()


# ------------------------------------------------------------
# IMPORTS — RUN ONLY AFTER AUTOMATIC SETUP
# ------------------------------------------------------------

import re
import sqlite3

import fitz
import streamlit as st
import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline


# ------------------------------------------------------------
# STREAMLIT CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="PDF Research Assistant",
    page_icon="📄",
    layout="wide",
)

DB_PATH = PROJECT_DIRECTORY / "document_data.db"

SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
SEMANTIC_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ------------------------------------------------------------
# MODEL LOADING
# ------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_models():
    """
    Download the models automatically on the first run and
    load them from the local cache on later runs.
    """
    device = 0 if torch.cuda.is_available() else -1

    summarization_pipeline = pipeline(
        task="summarization",
        model=SUMMARIZATION_MODEL,
        device=device,
    )

    embedding_model = SentenceTransformer(SEMANTIC_MODEL)

    return summarization_pipeline, embedding_model


with st.spinner(
    "Loading AI models. The first launch may take several minutes..."
):
    try:
        summarizer, semantic_model = load_models()
    except Exception as error:
        st.error(f"Unable to load the AI models: {error}")
        st.info(
            "Check the internet connection and available disk space, "
            "then restart the application."
        )
        st.stop()


# ------------------------------------------------------------
# PDF PROCESSING
# ------------------------------------------------------------

def extract_text_from_pdf(pdf_file):
    """Extract selectable text from an uploaded PDF."""
    file_bytes = pdf_file.getvalue()

    with fitz.open(stream=file_bytes, filetype="pdf") as document:
        pages = []

        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text("text").strip()

            if page_text:
                pages.append(
                    f"\n--- Page {page_number} ---\n{page_text}"
                )

    return "\n".join(pages).strip()


def clean_text(text):
    """Remove excessive whitespace while retaining paragraphs."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_and_segment_text(text):
    """Attempt to divide the document into named sections."""
    sections = {}
    current_section = "Introduction"

    for original_line in text.splitlines():
        line = original_line.strip()

        if not line:
            continue

        possible_heading = (
            len(line) <= 80
            and len(line.split()) <= 10
            and not line.endswith((".", ",", ";", ":"))
            and (
                line.isupper()
                or re.fullmatch(
                    r"(?:\d+(?:\.\d+)*\.?\s+)?"
                    r"[A-Z][A-Za-z0-9'&()/\-]*"
                    r"(?:\s+[A-Z][A-Za-z0-9'&()/\-]*)*",
                    line,
                )
            )
        )

        if possible_heading:
            current_section = line
            sections.setdefault(current_section, [])
        else:
            sections.setdefault(current_section, []).append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
        if "\n".join(content).strip()
    }


def save_to_database(data):
    """Store extracted sections in SQLite."""
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

        cursor.execute("DELETE FROM document_sections")

        cursor.executemany(
            """
            INSERT INTO document_sections (section, content)
            VALUES (?, ?)
            """,
            list(data.items()),
        )

        connection.commit()


# ------------------------------------------------------------
# TOKEN-AWARE SUMMARIZATION
# ------------------------------------------------------------

def create_model_chunks(text, maximum_tokens=850):
    """
    Split text using the model tokenizer instead of character
    counts. BART accepts approximately 1,024 input tokens.
    """
    tokenizer = summarizer.tokenizer

    token_ids = tokenizer.encode(
        text,
        add_special_tokens=False,
        truncation=False,
    )

    chunks = []

    for start in range(0, len(token_ids), maximum_tokens):
        chunk_ids = token_ids[start:start + maximum_tokens]

        chunk_text = tokenizer.decode(
            chunk_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        ).strip()

        if chunk_text:
            chunks.append(chunk_text)

    return chunks


def summarize_chunk(chunk, detailed=False):
    """Summarize one safe-sized chunk."""
    word_count = len(chunk.split())

    if word_count < 35:
        return chunk

    if detailed:
        maximum_length = min(180, max(70, word_count // 2))
        minimum_length = min(60, maximum_length - 10)
    else:
        maximum_length = min(90, max(40, word_count // 3))
        minimum_length = min(30, maximum_length - 10)

    result = summarizer(
        chunk,
        max_length=maximum_length,
        min_length=minimum_length,
        do_sample=False,
        truncation=True,
    )

    return result[0]["summary_text"].strip()


def summarize_text(text, summary_type="Short"):
    """Generate a summary of the complete PDF."""
    chunks = create_model_chunks(text)

    if not chunks:
        return "No text was available for summarization."

    # Short summaries use up to four document chunks.
    # Detailed summaries cover up to twelve chunks.
    chunk_limit = 4 if summary_type == "Short" else 12
    selected_chunks = chunks[:chunk_limit]

    summaries = []

    progress = st.progress(0, text="Preparing summary...")

    for index, chunk in enumerate(selected_chunks):
        summary = summarize_chunk(
            chunk,
            detailed=(summary_type == "Detailed"),
        )

        summaries.append(summary)

        percentage = int(
            ((index + 1) / len(selected_chunks)) * 100
        )

        progress.progress(
            percentage,
            text=(
                f"Summarizing section {index + 1} "
                f"of {len(selected_chunks)}..."
            ),
        )

    progress.empty()

    combined_summary = "\n\n".join(summaries)

    # Condense the partial summaries into one coherent short summary.
    if summary_type == "Short" and len(summaries) > 1:
        combined_words = len(combined_summary.split())

        if combined_words >= 50:
            try:
                combined_summary = summarizer(
                    combined_summary,
                    max_length=160,
                    min_length=60,
                    do_sample=False,
                    truncation=True,
                )[0]["summary_text"].strip()
            except Exception:
                # The partial summaries remain usable if the
                # second summarization pass fails.
                pass

    return combined_summary


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "structured_data" not in st.session_state:
    st.session_state.structured_data = {}

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None


# ------------------------------------------------------------
# USER INTERFACE
# ------------------------------------------------------------

st.title("📄 PDF Research Assistant")

st.caption(
    "Upload a text-based PDF and generate a local AI summary. "
    "No paid API or API key is required."
)

uploaded_file = st.file_uploader(
    "📂 Upload a PDF",
    type=["pdf"],
)

if uploaded_file is not None:
    file_identity = (
        uploaded_file.name,
        uploaded_file.size,
    )

    if st.session_state.processed_file != file_identity:
        with st.spinner("Extracting and processing the PDF..."):
            try:
                extracted_text = extract_text_from_pdf(uploaded_file)
                extracted_text = clean_text(extracted_text)

                if not extracted_text:
                    st.error(
                        "No selectable text was found. This may be a "
                        "scanned PDF, which requires OCR."
                    )
                    st.stop()

                structured_data = clean_and_segment_text(
                    extracted_text
                )

                save_to_database(structured_data)

                st.session_state.pdf_text = extracted_text
                st.session_state.structured_data = structured_data
                st.session_state.processed_file = file_identity

                st.success("✅ PDF processed successfully!")

            except Exception as error:
                st.error(f"Unable to process the PDF: {error}")
                st.stop()

    st.info(
        f"Extracted {len(st.session_state.pdf_text):,} characters "
        f"across {len(st.session_state.structured_data)} sections."
    )

    summary_type = st.radio(
        "📌 Summary type",
        options=["Short", "Detailed"],
        horizontal=True,
    )

    if st.button(
        "📜 Generate Summary",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner(
            "Generating the summary. CPU processing may take time..."
        ):
            try:
                summary = summarize_text(
                    st.session_state.pdf_text,
                    summary_type=summary_type,
                )

                st.subheader("📝 Summary")
                st.write(summary)

            except Exception as error:
                st.error(f"Unable to generate the summary: {error}")

    with st.expander("View extracted document sections"):
        for section, content in (
            st.session_state.structured_data.items()
        ):
            st.markdown(f"### {section}")
            st.write(content[:3000])

else:
    st.info("Upload a PDF to begin.")


st.divider()

st.markdown("## 📩 Contact Me")
st.markdown(
    "[✉️ Send Email](mailto:dasdevanshi7@gmail.com)"
)