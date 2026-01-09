# JobCheck – Fake Job Detection using AI & NLP
### B.Tech Final Year Project Report

---

## 1. Project Overview
**Goal**: To build a full-stack automated system that detects whether a job posting is **Real** or **Fake** using Natural Language Processing (NLP) and Machine Learning (ML).

**Problem Statement**: Fake job postings are a growing scam in India, duping millions of students. Manual verification is impossible. This project automates the detection process.

**Approach**: 
We utilize a **Hybrid Approach** combining:
1.  **Machine Learning**: Logistic Regression trained on TF-IDF vectors for general textual patterns.
2.  **Rule-Based Heuristics**: A custom expert system to catch Indian-context scams (e.g., "security deposit", "12th pass 50k salary") that global datasets often miss.

---

## 2. Technical Architecture (Milestones)

The project is structured into 4 logical milestones:

### 🔹 Milestone 1: Data Preprocessing & EDA
*   **Inputs**: Raw dataset (`fake_job_postings.csv`).
*   **Process**:
    *   Text Cleaning (Removing HTML tags, special characters).
    *   NLP Pipeline: Tokenization $\rightarrow$ Stopword Removal $\rightarrow$ Lemmatization.
    *   Feature Extraction: Converted text to numbers using **TF-IDF Vectorization**.
*   **Output**: Cleaned data saved to `processed_data/`.

### 🔹 Milestone 2: Model Training
*   **Models Tested**:
    1.  **Logistic Regression** (Selected for speed & interpretability).
    2.  **Random Forest** (Comparison baseline).
*   **Result**: Achieved **~97% Accuracy** on test data.
*   **Artifacts**: Saved trained model (`logistic_regression.pkl`) and vectorizer.

### 🔹 Milestone 3: Intelligent Backend & Feedback Loop
*   **Tech Stack**: Python **FastAPI**, **SQLite**.
*   **Innovation**: 
    1.  **Hybrid Prediction**: ML + Heuristic Rules.
    2.  **Feedback System**: Users can "Flag" incorrect predictions.
    3.  **Database**: Stores all predictions and flags for future retraining.

### 🔹 Milestone 4: Admin Dashboard & Frontend
*   **Tech Stack**: HTML5, CSS3, JS.
*   **Features**:
    *   **User Interface**: Clean prediction UI with Flagging button.
    *   **Admin Panel**: (`admin.html`) Dashboard showing real-time statistics (False Positives, Total Scans).
    *   **Analytics**: Tracks detection rates and user reports.

---

## 3. Deep Learning Experimentation (Milestone 2B)
While the production app uses **Random Forest** for speed, we developed a **BiLSTM (Bidirectional LSTM)** model using TensorFlow/Keras to explore deep learning capabilities.
*   **Architecture**: Embedding Layer $\rightarrow$ BiLSTM $\rightarrow$ Dense Layer.
*   **Code**: `train_deep_learning.py`.

---

## 4. Challenges Faced & Solutions
*(This section is excellent for your Viva/Interview)*

| Challenge | Impact | Solution Implemented |
| :--- | :--- | :--- |
| **Missing Context** | The ML model originally predicted "Real" for scams like "Work from home, 70k/month". | **Hybrid Layer**: Added specific rule-checks for high-risk phrases like *"home-based data processing"* before calling the model. |
| **False Positives** | Legitimate jobs with "Salary per month" were getting flagged as Fake. | **Logic Refinement**: Improved rules to check context (e.g., allow "per month" if it's describing salary, but flag if used with "guaranteed income"). |
| **Pipeline Errors** | The backend initially crashed because it received raw text but the model expected numbers. | **Pipeline Integration**: Updated `app.py` to load and apply the **TF-IDF Vectorizer** to incoming text before prediction. |

---

## 4. How to Run the Project

### Prerequisites
*   Python 3.8+
*   Virtual Environment (Recommended)

### Step 1: Start the Backend server
Open your terminal in the `milestone3_api` folder and run:
```bash
uvicorn app:app --reload
```
*You will see: `Uvicorn running on http://127.0.0.1:8000`*

### Step 2: Launch the Frontend
*   Go to the `milestone4_frontend` folder.
*   Open `index.html` in Chrome/Edge.

### Step 3: Test
*   Paste any job description and click **"Check Job"**.

---

## 5. Future Scope
*   **Web Scraping**: Automatically verify company names from LinkedIn/Google.
*   **Deep Learning**: Implement LSTM/BERT for better context understanding.
*   **Browser Extension**: A chrome plugin to flag fake jobs directly on Naukri/Indeed.

---
*Verified and Validated by AI Project Mentor.*
