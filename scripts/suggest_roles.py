from openai import OpenAI
import yaml
from pathlib import Path

api_key = yaml.safe_load(open("config/credentials.yaml"))["openai_api_key"]
client = OpenAI(api_key=api_key)

def suggest_roles_from_cv(cv_text):
    PROMPT = f"""
    Extract professional strengths and suggest suitable job roles based on this resume:

    {cv_text}

Respond only with 5 most relevant job role titles (e.g., "Data Scientist", "Machine Learning Engineer"), without numbering or industry names, one per line.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": PROMPT}]
    )
    return response.choices[0].message.content


def main():
    with open("data/cv_parsed.txt", "r", encoding="utf-8") as f:
        cv_text = f.read()
    roles = suggest_roles_from_cv(cv_text)
    with open("data/suggested_roles.txt", "w") as f:
        f.write(roles)
    print("[✔] Suggested roles saved to: data/suggested_roles.txt")

if __name__ == "__main__":
    main()
