import json
from datetime import datetime, timedelta
from pathlib import Path
import re
import unicodedata

RAW_JOBS_PATH = "data/raw_jobs.json"
HISTORY_PATH = "data/jobs_history.json"

def is_recent(post_date):
    job_time = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S")
    return datetime.now() - job_time < timedelta(hours=24)

def clean_description(description: str) -> str:
    if not description:
        return ""

    # Fix double encoding artifacts like \u00e2\u0080\u0093
    try:
        description = bytes(description, "utf-8").decode("utf-8", errors="replace")
    except Exception:
        pass

    # Replace problematic Unicode characters
    substitutions = {
        "\u2019": "'",  # right single quote
        "\u2018": "'",  # left single quote
        "\u201c": "\"",  # left double quote
        "\u201d": "\"",  # right double quote
        "\u2022": "-",  # bullet
        "\u2013": "-",  # en-dash
        "\u2014": "-",  # em-dash
        "\u00a0": " ",  # non-breaking space
        "\u00c2": "",   # common artifact
        "\u00e2\u0080\u0093": "-",  # special dash
        "\u00e2\u0080\u0099": "'",  # apostrophe
    }
    for bad, good in substitutions.items():
        description = description.replace(bad, good)

    # Strip accents and normalize
    description = unicodedata.normalize("NFKD", description)
    description = "".join(c for c in description if unicodedata.category(c) != 'Mn')

    # Remove boilerplate patterns
    patterns_to_remove = [
        r"What we offer you:.*",
        r"Benefits.*",
        r"Additional Information.*",
        r"Privacy Statement.*",
        r"DBS and background checks.*",
        r"This role is subject to.*",
        r"We offer a competitive basic salary.*",
    ]
    for pattern in patterns_to_remove:
        description = re.sub(pattern, "", description, flags=re.IGNORECASE | re.DOTALL)

    # Collapse multiple spaces and remove newlines
    description = re.sub(r"\s+", " ", description).strip()

    return description

def main(log_step=None):
    with open(RAW_JOBS_PATH) as f:
        jobs = json.load(f)

    history = {}
    if Path(HISTORY_PATH).exists():
        with open(HISTORY_PATH) as f:
            history = json.load(f)

    new_jobs = []
    for job in jobs:
        job_id = job.get("url")
        if job_id not in history and is_recent(job.get("posted", "1970-01-01T00:00:00")):
            job["description"] = clean_description(job.get("description", ""))
            new_jobs.append(job)
            history[job_id] = job.get("posted")

    with open("data/filtered_jobs.json", "w") as f:
        json.dump(new_jobs, f, indent=2)

    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
    
    if log_step:
        log_step(f"✔ {len(jobs) - len(new_jobs)} redundant jobs removed.", overwrite_last=True)
        log_step(f"✔ {len(new_jobs)} new jobs saved.")

    print(f"[✔] {len(new_jobs)} new jobs saved to data/filtered_jobs.json")

if __name__ == "__main__":
    main()