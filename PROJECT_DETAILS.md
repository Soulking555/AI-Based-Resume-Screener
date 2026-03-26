# AI Hiring Intelligence Platform - Complete Technical Details

## 1. Overview
The AI Hiring Intelligence Platform is an end-to-end full-stack solution designed to automate the technical recruitment screening process. Unlike typical "black-box" Applicant Tracking Systems (ATS), this platform prioritizes explainability, semantic understanding, and actionable insights.

## 2. Software & Apps
### Front-End Application
*   **Frameworks & Libraries:** React (v19) and Vite for build tooling.
*   **Styling:** Custom Vanilla CSS utilizing variables for a dynamic dark-mode-first modern recruiter environment.
*   **Role:** Acts as the recruiter dashboard where PDFs are uploaded, job requirements are defined, scored candidate metrics are visualized, and skill gaps are explicitly highlighted.

### Back-End Application
*   **Frameworks & Server:** FastAPI (Python), run via `uvicorn` (ASGI server).
*   **Role:** Handles highly concurrent REST API requests encompassing PDF processing, AI inference (vector similarity, NLP entity recognition), scoring, clustering, and interview question generation.
*   **Database Integration:** MongoDB (migrated from SQLite) accessed via `pymongo`. Transitioning to MongoDB allowed better handling of document-based unstructured JSON data, such as candidate metrics, dynamically grouped skills, and clustering labels. `pydantic` rigidly enforces schema validations.
*   **File Uploads:** `python-multipart` is used for handling the stream of candidate resumes over form data.

## 3. Core AI Libraries & Tools
*   **`pdfplumber`:** Used for robust and precise text extraction from uploaded PDF resumes.
*   **`spaCy`:** Forms the backbone of the NLP pipeline, heavily utilizing tokenization and custom Regex constraints against a dictionary of technical frameworks to extract entities (skills, education, projects).
*   **`sentence-transformers` (`all-MiniLM-L6-v2`):** Used as a semantic matching engine when literal keyword extraction fails. It computes cosine similarity across text chunks, recognizing that "ReactJS" and "React" are practically identical conceptually.
*   **`scikit-learn`:** Supports the autonomous machine learning components, specifically TF-IDF vectorization and K-Means clustering algorithm for categorizing broad candidate talent pools.

## 4. Methodology & Procedure
The pipeline operates in the following sequence from document ingestion to analytics generation:

1.  **Document Ingestion:** A recruiter uploads a batch of applicant PDFs and inputs the target job requirements via the React frontend. The files are securely streamed to the FastAPI backend.
2.  **Information Extraction:** `pdfplumber` rips the raw text from the PDFs. `spaCy` analyzes the linguistic structure, pulls out distinct capability entities, and matches them against the predefined taxonomy.
3.  **Semantic Context Matching:** When basic keyword mapping doesn't trigger (e.g. matching "Frontend architect" against an application that states "Built client UIs with modular JS"), the `SentenceTransformers` model steps in, running vector similarity analysis between the job description tokens and candidate capabilities.
4.  **Explainable Scoring Execution:** Rather than outputting an opaque numeric result, the AI engine builds a transparent evaluation module (see Algorithm section below), weighing specific sub-components independently.
5.  **Analytics & Storage:** Candidates are clustered, their explicit skill gaps are flagged, dynamic interview questions are generated to test on missing skills, and all of these detailed features are persisted into the MongoDB collection array. The React recruitment dashboard polls this data and updates the visual UI seamlessly.

## 5. Algorithms
The platform relies on several intertwined algorithmic breakthroughs designed to inject both accuracy and transparency into hiring:

### A. Explainable AI Scoring Algorithm
Instead of relying on a generalized "black-box" model output, a customized weighted heuristic equation calculates an aggregated scoring metric:
`Score = 0.4(Skill) + 0.2(Similarity) + 0.2(Experience) + 0.1(Education) + 0.1(Projects)`
*This algorithm visually separates Experience, Education, and Skills so a recruiter can review the dashboard and mathematically trace why one candidate scored an 85% versus a 60%.*

### B. Skill Gap Detection Logic
By executing a set difference computation (`Job Requirements` - `Candidate Capabilities`), the platform objectively determines missing technical competencies (e.g., "Missing: Docker, AWS"). Based on these explicit differences, actionable recommendations are surfaced for the recruiter and the technical interviewer.

### C. Resume Clustering (Unsupervised ML)
Rather than recruiters manually sorting hundreds of applications across different skill buckets, the system implements autonomous categorization:
*   **TF-IDF Vectorization:** The textual contents of all resumes are transformed into a mathematical matrix of features, algorithmically isolating important and unique terms specific to each document.
*   **K-Means Clustering:** `scikit-learn` groups the vectorized resumes into specialized `K` clusters using geometric distance calculation. This categorizes resumes natively into groupings like "Data Engineering", "Front End Web", etc., without requiring manual oversight.

### D. Targeted Interview Question Algorithm
Bridging the gap between tracking systems and actual interviews, the backend seamlessly outputs targeted technical interview questions utilizing the negative space uncovered during the `Skill Gap Detection` phase. If the candidate knows React but completely lacks standard database experience, the engine dynamically outputs structural questions focusing on SQL or NoSQL intuition, systematically probing the exact areas where the candidate is weakest.
