import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"].split(",")
EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(subject, html_body):
    msg = MIMEText(html_body, "html")
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    msg["Subject"] = subject

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_APP_PASSWORD)
        server.send_message(msg)

def main():
    with open("sample_data.json") as f:
        data = json.load(f)

    total = len(data)
    in_progress = [d for d in data if d["owner"] != "queue"]
    new = [d for d in data if d["owner"] == "queue"]

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    rows = ""
    for item in data:
        state = "IN_PROGRESS" if item["owner"] != "queue" else "NEW"
        rows += f"""
        <tr>
          <td>{item['id']}</td>
          <td>{item['title']}</td>
          <td>{state}</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family:Arial;background:#f5f5f5;padding:20px;">
      <h2>Daily Automation Report</h2>
      <p>Generated at {timestamp}</p>

      <ul>
        <li>Total items: {total}</li>
        <li>In Progress: {len(in_progress)}</li>
        <li>New: {len(new)}</li>
      </ul>

      <table border="1" cellpadding="6" cellspacing="0">
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>State</th>
        </tr>
        {rows}
      </table>
    </body>
    </html>
    """

    send_email("Daily Automation Report", html)
    print("Report sent successfully")

if __name__ == "__main__":
    main()
