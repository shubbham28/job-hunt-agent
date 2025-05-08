# 📄 Job Hunt Agent

An AI agent that automates job discovery, filtering, and ATS-based scoring using OpenAI and job search APIs. Complete with a modular backend and an interactive Streamlit dashboard.

## 🚀 Features

- 🔍 Parse your CV and extract key details
- 🧠 Suggest suitable roles via OpenAI GPT
- 🌍 Search real-time jobs across selected countries via JSearch API (LinkedIn, Google Jobs, etc.)
- ❎ Deduplicate similar jobs posted within 24 hours
- 📈 Score jobs for relevance using GPT-4 and rank by ATS fit
- 🖥 Interactive Streamlit dashboard for job hunting

## 📁 Folder Structure

```yaml
job_hunt_agent/
├── config/                    # API keys, credentials
│   └── credentials.yaml
├── cv_input/                  # Upload your CV here
│   └── your_cv.pdf
├── data/                      # Intermediate data files
│   ├── cv_parsed.txt
│   ├── suggested_roles.txt
│   ├── raw_jobs.json
│   ├── filtered_jobs.json
│   └── jobs_history.json
├── output/                    # Final job list with ATS scores
│   └── ats_ranked_jobs.csv
├── scripts/                   # Pipeline components
│   ├── parse_cv.py
│   ├── suggest_roles.py
│   ├── scrape_jobs.py
│   ├── deduplicate_jobs.py
│   ├── score_ats.py
│   └── main.py
├── utils/                     # Shared logic
│   ├── scrape_utils.py
├── main.py           # Main app UI
└── job_hunt_agent_notebook.ipynb  # Jupyter-based control
```

---

## 🔧 Installation

Install all requirements:

* `Python 3.8+`
* `streamlit`, `openai`, `requests`, `pandas`, `PyMuPDF`, `beautifulsoup4`, `PyYAML`

---

## 🔐 Credentials Setup

Create a `config/credentials.yaml` like this:

```yaml
openai_api_key: "your-openai-api-key"

jsearch:
  x_rapidapi_key: "your-rapidapi-key"
  x_rapidapi_host: "jsearch.p.rapidapi.com"
```

---

## 🧪 How to Use

### 🖥 Option 1: Use Streamlit App

```bash
streamlit run main.py
```

* Choose to upload a new CV or reuse the existing one
* Select countries from a dropdown
* Start the full pipeline
* View ATS scoring live
* Results shown in an interactive table with clickable application links

### 📘 Option 2: Use the Notebook

Open `job_hunt_agent_notebook.ipynb` and run:

* `parse_cv.main()`
* `suggest_roles.main()`
* `scrape_jobs.main()`
* `deduplicate_jobs.main()`
* `score_ats.score_ats()`

---

## 🤖 ATS Scoring

Each job is scored against your CV using GPT-3.5:

* Uses OpenAI to extract reasoning and a score (0–100)
* Only new jobs are scored
* Reasoning and scores are stored in `output/ats_ranked_jobs.csv`

---

## ✅ Built-in Safeguards

* ⏱ Skips jobs already processed
* 🔁 Avoids scraping duplicates within 24h
* 🚫 Stops if no jobs found after deduplication

---

## 👨‍💻 Author

**Shubbham Gupta**
PhD in Data Science | AI & Automation Developer
🔗 [LinkedIn](https://linkedin.com/in/shubbhamgupta) • 🧠 Focused on AI for productivity and personalization
