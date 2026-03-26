# AI Hiring Intelligence Platform with Explainable Resume Screening and Skill Gap Detection

## 1. Abstract
The hiring process for technical roles is increasingly overwhelmed by the sheer volume of applicants, making manual resume screening inefficient and prone to bias. Existing automated resume parsers primarily rely on exact keyword matching, which fails to capture semantic meaning and often acts as a opaque "black box" that rejects qualified candidates without explanation. This paper proposes a novel AI Hiring Intelligence Platform that integrates Natural Language Processing (NLP), semantic analysis via Sentence Transformers, Explainable AI (XAI) scoring, and Scikit-learn KMeans resume clustering. The resulting system not only extracts text efficiently but provides recruiters with an interpretable, weighted score breakdown (Skill, Similarity, Experience, Education, Projects), explicitly highlights skill gaps, and autonomously generates targeted technical interview questions. 

## 2. Introduction
Recruitment in the modern digital era faces a critical bottleneck: the initial screening phase. Recruiters receive hundreds of applications per job posting, but lack the technical depth to accurately assess intricate software engineering syntax and frameworks. While Applicant Tracking Systems (ATS) have automated parsing, they fall short in three major ways:
1. **Lack of Explainability**: ATS algorithms provide a match percentage without detailing *why* a candidate scored that metric.
2. **Semantic Blindness**: ATS relies on literal keyword matching (e.g., rejecting a candidate with "ReactJS" when "React" was requested).
3. **Absence of Actionable Insights**: Systems do not natively highlight missing competencies or help recruiters probe for those weaknesses during interviews.

Our proposed system bridges these gaps by providing an intelligent, transparent hiring assistant.

## 3. Literature Survey

| Paper | Method | Problem Identified | Our Proposed Improvement |
|---|---|---|---|
| Paper 1 | Keyword matching (TF-IDF) | No semantic understanding of skills | Added BERT/Sentence-Transformers for contextual similarity mapping. |
| Paper 2 | NLP-based scoring models | Lack of explainability / Black-box scoring | Implemented XAI breakdown visually separating Experience, Education, and Skills. |
| Paper 3 | Supervised Resume ranking | No skill gap identification | Added Skill Gap Detection and autonomous Interview Question Generation. |
| Paper 4 | Rule-based ATS | Rigid, unscalable architecture | Resume clustering via Scikit-learn KMeans to naturally group talent pools. |

## 4. Methodology
The pipeline architecture is composed of sequential modules designed for parsing, extracting, matching, and presentation:
1. **Document Ingestion**: PDF files are uploaded and processed using `pdfplumber` for robust text extraction.
2. **Information Extraction**: We utilize `spaCy` alongside Regex constraints for entity recognition, matched against a diverse dictionary of technical frameworks.
3. **Semantic Matching Engine**: If exact keyword constraints fail, `all-MiniLM-L6-v2` Sentence Transformers compute cosine similarity between the job description tokens and candidate capabilities.
4. **Scoring Function**: The Explainable AI module computes the weighted sum: `Score = 0.4(Skill) + 0.2(Similarity) + 0.2(Experience) + 0.1(Education) + 0.1(Projects)`.

## 5. Proposed System
Our system's novelty stems from four core innovations designed to prioritize transparency and intelligence:
1. **Skill Gap Intelligence**: By computing the set difference between Job Requirements and Candidate capabilities, the platform highlights explicit weaknesses (e.g., "Missing: Docker") and generates actionable recommendations ("Learn Docker").
2. **Explainable AI Scoring**: The recruiter is shielded from complex ML output. Instead, numerical scores are divided visually on a React Dashboard, enabling the recruiter to quickly see that the candidate lacked education but over-indexed on raw skills.
3. **Resume Clustering**: Applying Scikit-learn K-Means over TF-IDF vectors categorizes resumes autonomously into specialized pools (e.g., "Web Developers", "Data Scientists") without manual tagging.
4. **Interview Question Generation**: Using the identified skill gaps, the backend generates dynamic technical questions to test a candidate’s problem-solving intuition for technologies they lack.

## 6. Implementation
The platform acts as a cohesive full-stack software application:
* **Frontend**: React and Vite, utilizing custom Vanilla CSS variables for a dynamic, dark-mode-first modern recruiter environment.
* **Backend**: FastAPI (Python) serving highly concurrent requests for PDF processing.
* **Database**: SQLite integrated with Pydantic for rigid schema enforcement and relational tracking of Jobs, Candidates, and Screening Results.
* **AI Tooling**: `spaCy`, `SentenceTransformers`, `scikit-learn`, and `pdfplumber`.

## 7. Results
During synthetic internal testing, the AI logic evaluated permutations of resumes against predefined Software Engineering requisitions.
* **Speed**: End-to-end PDF processing, text extraction, matrix similarity computation, and database insertion executed in <2.5 seconds per resume on average.
* **Accuracy**: The Explainable logic accurately penalized candidates missing core "Must-have" attributes while rewarding conceptually identical skills (e.g., "ReactJS" matched closely to "React").
* **Ranking Quality**: The weighted heuristic reliably pushed experienced Full-Stack developers to the top of the pool (>85% scores), automatically labeling them "Shortlisted", and successfully isolated missing skills for Junior developers.

## 8. Conclusion
The AI Hiring Intelligence Platform completely reimagines the initial Applicant Tracking System by favoring explainability over obfuscation. By detailing exactly why a candidate received a 72% matching score and presenting targeted interview questions, it empowers recruiters to make highly informed, unbiased, and deeply technical decisions rapidly. 

## 9. Future Work
Future iterations of this platform will explore:
* **LLM Integration**: Integrating localized Large Language Models (e.g., Llama 3) to summarize the candidate's career trajectory into a concise narrative paragraph.
* **Video Resume Analysis**: Extracting soft skills, tone, and communication capabilities from candidate introduction videos using multi-modal transformer networks.
* **Bias Mitigation Filters**: Training anomaly detection models to flag resumes evaluated with potential geographic or demographic bias.
