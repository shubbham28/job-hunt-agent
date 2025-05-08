import smtplib
import yaml
import pandas as pd
from email.message import EmailMessage

config = yaml.safe_load(open("config/credentials.yaml"))['email']
df = pd.read_csv("output/ats_ranked_jobs.csv")

msg = EmailMessage()
msg["Subject"] = "Ranked Job List by ATS Score"
msg["From"] = config['sender']
msg["To"] = config['receiver']
msg.set_content("Find attached the ranked job list.")

with open("output/ats_ranked_jobs.csv", "rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename="ats_ranked_jobs.csv")

server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
server.starttls()
server.login(config['sender'], config['password'])
server.send_message(msg)
server.quit()
print("[✔] Email sent with ranked job list.")
