import streamlit as st
import json
import pandas as pd
from openai import OpenAI
import yaml
from pathlib import Path

def score_ats(log_step=None):
    # Load OpenAI API key
    api_key = yaml.safe_load(open("config/credentials.yaml"))["openai_api_key"]
    client = OpenAI(api_key=api_key)

    # Load CV text
    with open("data/cv_parsed.txt", "r", encoding="utf-8") as f:
        cv_text = f.read()

    # Load filtered job list
    with open("data/filtered_jobs.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    # Load existing scored jobs (if any)
    output_path = Path("output/ats_ranked_jobs.csv")
    existing_urls = set()
    existing_rows = []

    if output_path.exists():
        existing_df = pd.read_csv(output_path)
        existing_urls = set(existing_df["url"])
        existing_rows = existing_df.to_dict(orient="records")
    progress = st.empty()
    results = []
    for i, job in enumerate(jobs):
        if log_step:
            log_step(f"📊 ATS score calculating for job {i+1}/{len(jobs)}", overwrite_last=True)
        print(f"📊 ATS score calculating for job {i+1}/{len(jobs)}")
        prompt = f"""
You are an AI applicant tracking system. Match the following CV to the job description and assign an ATS score from 0 to 100.
Explain your reasoning in 1–2 lines, then give only the score.

CV:
{cv_text}

Job Description:
{job['description']}

Output Format:
Reasoning: <your reasoning>
ATS Score: <score>
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        lines = reply.splitlines()

        reasoning_line = next((line for line in lines if line.lower().startswith("reasoning:")), "")
        score_line = next((line for line in lines if "ATS Score:" in line), "ATS Score: 0")

        # Extract values
        reasoning_text = reasoning_line.replace("Reasoning:", "").strip()
        try:
            ats_score = int(score_line.split(":")[1].strip())
        except:
            ats_score = 0
        job["ats_score"] = ats_score
        job["ats_reasoning"] = reasoning_text
        results.append(job)


    # Save to CSV
    all_results = existing_rows + results
    df = pd.DataFrame(all_results)
    print(df)
    Path("output").mkdir(exist_ok=True)
    df.to_csv("output/ats_ranked_jobs.csv", index=False)
    print("✅ ATS-ranked job list saved to output/ats_ranked_jobs.csv")

