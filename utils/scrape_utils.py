import requests
from datetime import datetime

def login_and_scrape_jobs(config, roles, countries):
    """
    Use Jsearch API (via RapidAPI) to get job listings across major platforms.
    Filters results from the last 24 hours.
    """
    headers = {
        "X-RapidAPI-Key": config["jsearch"]["x_rapidapi_key"],
        "X-RapidAPI-Host": config["jsearch"]["x_rapidapi_host"]
    }

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    results = []

    for role in roles:
        for country in countries:
            query = f"{role} in {country}"
            url = "https://jsearch.p.rapidapi.com/search"

            params = {
                "query": query,
                "page": "1",
                "num_pages": "1",  # You can increase pages if needed
                "date_posted": "today"
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json().get("data", [])
                for job in data:
                    results.append({
                        "title": job.get("job_title", "Unknown"),
                        "company": job.get("employer_name", "Unknown"),
                        "url": job.get("job_apply_link", job.get("job_google_link", "")),
                        "posted": now,
                        "description": job.get("job_description", "")
                    })

    return results
