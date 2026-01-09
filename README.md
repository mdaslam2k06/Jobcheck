# 🔍 JobCheck: Fake Job Detection System

**JobCheck** is an AI-powered Full-Stack application designed to detect fraudulent job postings using Natural Language Processing (NLP) and Machine Learning. 

> *Developed as part of the Infosys Springboard Virtual Internship.*

![Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green)
![ML](https://img.shields.io/badge/Model-Random%20Forest-orange)

## 🚀 Features

*   **Hybrid Detection Logic**: Combines **Random Forest Classifier** (for pattern recognition) with **Heuristic Rules** (for catching specific scams like "security deposit").
*   **Intelligent Backend**: FastAPI server that handles predictions and updates immediately.
*   **Flagging System**: Users can report incorrect predictions, creating a feedback loop for future retraining.
*   **Admin Dashboard**: A hidden, secure panel for administrators to view statistics (`Real vs Fake` ratios) and manage user flags.
*   **Deep Learning (Experimental)**: Includes a Bi-Directional LSTM implementation for advanced context understanding.

## 🛠️ Tech Stack

*   **Frontend**: HTML5, CSS3, JavaScript (Vanilla).
*   **Backend**: Python, FastAPI, Uvicorn.
*   **Database**: SQLite (Lightweight, Serverless).
*   **Machine Learning**: Scikit-Learn (`RandomForestClassifier`, `LogisticRegression`), TF-IDF Vectorization.
*   **Deep Learning**: TensorFlow/Keras (BiLSTM).

## 📂 Project Structure

```
JOBCHECK/
├── milestone2_models/      # Saved ML Models (.pkl)
├── milestone3_api/         # Backend Code
│   ├── app.py              # Main API Server
│   └── database.py         # Database Handler
├── milestone4_frontend/    # User Interface
│   ├── index.html          # Main User Page
│   ├── admin.html          # Admin Dashboard
│   └── style.css           # Styling
├── processed_data/         # Cleaned Datasets
├── train_deep_learning.py  # DL Model Script
└── README.md               # Documentation
```

## ⚡ How to Run

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/shreyaspandey0/JobCheck-Fake-Job-Detection.git
    cd JobCheck-Fake-Job-Detection
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start Backend**
    ```bash
    cd milestone3_api
    uvicorn app:app --reload
    ```

4.  **Launch Frontend**
    *   Open `milestone4_frontend/index.html` in your browser.

## 🛡️ Admin Access

To access the Admin Dashboard:
1.  Navigate manually to `/admin.html` in your browser.
2.  Login using default credentials (Check `database.py` or project report).

## 📜 License

This project is for educational purposes under the Infosys Springboard Internship program.

---
*Created by Shreyash Pandey*
