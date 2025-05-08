import streamlit as st
import os
import shutil
import json
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime
from scripts import parse_cv, suggest_roles, scrape_jobs, deduplicate_jobs, score_ats

DATA_DIR = Path("data")
CV_PATH = DATA_DIR / "cv_parsed.txt"
ATS_CSV_PATH = Path("output/ats_ranked_jobs.csv")

st.set_page_config(page_title="Job Hunt Agent", layout="wide")
st.title("🤖 Job Hunt Agent Dashboard")

# --- STEP 1: CHOOSE CV ---
st.header("📄 Upload CV or Use Existing")

cv_choice = st.radio("Select CV option:", ["Upload new CV", "Use previous CV"])

if cv_choice == "Upload new CV":
    uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
    if uploaded_file:
        cv_dir = Path("cv_input")
        cv_dir.mkdir(exist_ok=True)
        new_cv_path = cv_dir / "your_cv.pdf"
        with open(new_cv_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("✅ New CV uploaded.")
        is_new_cv = True
    else:
        st.stop()
else:
    if not CV_PATH.exists():
        st.error("❌ No existing parsed CV found. Please upload one.")
        st.stop()
    new_cv_path = Path("cv_input/your_cv.pdf")
    is_new_cv = False

    st.header("🌍 Select Countries for Job Search")

country_options = [
    "Ireland", "United Kingdom", "United States", "Germany",
    "France", "Netherlands", "Canada", "India", "Remote"
]

selected_countries = st.multiselect(
    "Select countries to search for jobs:",
    options=country_options,
    default=["Ireland", "United Kingdom"]
)

# --- STEP 2: RUN PIPELINE ---
st.header("🚀 Run Job Hunt Pipeline")

if st.button("Start Job Search"):
    if not selected_countries:
        st.warning("Please select at least one country before starting the job search.")
        st.stop()

    log_container = st.empty()
    logs = []

    def log_step(text, overwrite_last=False):
        if overwrite_last and logs:
            logs[-1] = text
        else:
            logs.append(text)
        log_container.code("\n".join(logs), language="bash")


    log_step("[1] Parsing CV...")
    parse_cv.main()
    log_step("✔ CV parsed.")

    log_step("[2] Suggesting roles...")
    suggest_roles.main()
    log_step("✔ Roles suggested.")

    log_step("[3] Scraping jobs...")
    scrape_jobs.main(log_step=log_step,countries = selected_countries)

    log_step("[4] Getting unique jobs...")
    log_step("[4] Getting unique jobs...")
    deduplicate_jobs.main(log_step=log_step)
    
    with open("data/filtered_jobs.json", "r", encoding="utf-8") as f:
        filtered_jobs = json.load(f)

    if len(filtered_jobs) == 0:
        log_step("❌ No new jobs found to score. Job hunt stopped.")
        st.warning("No new jobs available for scoring. Try updating your CV or waiting for new postings.")
        st.stop()
    
    log_step("[5] Scoring jobs via OpenAI GPT...")
    log_step("[5] Scoring jobs via OpenAI GPT...")
    score_ats.score_ats(log_step=log_step)
    log_step("✔ ATS scoring complete.")

    st.success("🎯 Pipeline finished.")

    # --- STEP 3: SHOW RESULTS ---
    st.header("📊 Top Matching Jobs")

    if ATS_CSV_PATH.exists():
        df = pd.read_csv(ATS_CSV_PATH)
        df = df.sort_values(by="ats_score", ascending=False)

        # Make URL clickable
        def make_clickable(url):
            return f'<a href="{url}" target="_blank">Apply</a>'

        df["apply"] = df["url"].apply(make_clickable)
        df_display = df[["title", "company", "posted", "ats_score", "apply", "ats_reasoning"]].copy()
        df_display.rename(columns={
            "title": "Job Title",
            "company": "Company",
            "posted": "Date Posted",
            "ats_score": "ATS Score",
            "apply": "Application Link",
            "ats_reasoning": "GPT Match Justification"
        }, inplace=True)
        st.markdown("<h3 style='text-align: center;'>Top results (sorted by ATS score)</h3>", unsafe_allow_html=True)
        st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.warning("No results to display.")
