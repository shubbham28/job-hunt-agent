import yaml
from pathlib import Path
from utils.scrape_utils import login_and_scrape_jobs

def main(log_step=None,countries = ["Ireland", "United Kingdom"]):
    config = yaml.safe_load(open("config/credentials.yaml"))

    #countries = ["Ireland", "United Kingdom", "Europe"]

    with open("data/suggested_roles.txt") as f:
        roles = [line.strip("- ") for line in f if line.strip()]

    jobs = login_and_scrape_jobs(config, roles, countries)
    Path("data").mkdir(exist_ok=True)

    with open("data/raw_jobs.json", "w") as f:
        import json
        json.dump(jobs, f, indent=2)
    if log_step:
        log_step(f"✔ Scraped {len(jobs)} jobs.")
    print(f"[✔] Scraped {len(jobs)} jobs saved to data/raw_jobs.json")
    
    
if __name__ == "__main__":
    main()