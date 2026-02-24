import os
import requests
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

# Load configuration
load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")
GMAIL_PASS = os.getenv("GMAIL_PASS")
PROJECT_KEY = "KAN"


def get_issues(jql):
    """Fetch issues and return clickable HTML list."""
    auth = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_TOKEN}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    url = f"{JIRA_URL}/rest/api/3/search/jql"
    payload = {"jql": jql, "maxResults": 50, "fields": ["summary", "key"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        issues = response.json().get("issues", [])

        issue_list = ""
        for issue in issues:
            link = f"{JIRA_URL}/browse/{issue['key']}"
            issue_list += f"""
            <li>
                <a href="{link}" style="color:#0052CC; text-decoration:none; font-weight:bold;">
                    {issue['key']}
                </a>
                – {issue['fields']['summary']}
            </li>
            """

        return len(issues), issue_list

    except Exception as e:
        print(f"Error fetching Jira data: {e}")
        return 0, "<li>Error retrieving list.</li>"


def main():
    if not all([JIRA_EMAIL, JIRA_TOKEN, GMAIL_PASS, JIRA_URL]):
        print("Missing environment variables in .env file.")
        return

    count_created, list_created = get_issues(
        f"project={PROJECT_KEY} AND created >= -7d"
    )
    count_resolved, list_resolved = get_issues(
        f"project={PROJECT_KEY} AND resolved >= -7d"
    )
    count_open, list_open = get_issues(
        f"project={PROJECT_KEY} AND statusCategory != Done"
    )

    # HTML Report
    html_report = f"""
    <html>
    <body style="font-family:Arial, sans-serif; background:#f4f6f8; padding:20px;">
    <div style="background:white; padding:20px; border-radius:8px;">

    <h2 style="color:#172B4D;">Jira Weekly Status Report – {PROJECT_KEY}</h2>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

    <hr>

    <h3>Summary Stats</h3>
    <ul>
        <li><strong>Issues Created (Last 7 Days):</strong> {count_created}</li>
        <li><strong>Issues Resolved (Last 7 Days):</strong> {count_resolved}</li>
        <li><strong>Total Currently Open:</strong> {count_open}</li>
    </ul>

    <h3>Created This Week</h3>
    <ul>
        {list_created}
    </ul>

    <h3>Currently Open</h3>
    <ul>
        {list_open}
    </ul>

    </div>
    </body>
    </html>
    """

    # Send HTML Email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Weekly Jira Report - {PROJECT_KEY}"
    msg["From"] = JIRA_EMAIL
    msg["To"] = JIRA_EMAIL

    msg.attach(MIMEText(html_report, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(JIRA_EMAIL, GMAIL_PASS)
            server.send_message(msg)
            print("Senior-level HTML report sent successfully.")
    except Exception as e:
        print(f"SMTP Error: {e}")


if __name__ == "__main__":
    main()
