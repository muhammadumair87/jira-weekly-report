import os
import requests
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")
GMAIL_PASS = os.getenv("GMAIL_PASS")
PROJECT_KEY = "KAN"


def get_issues(jql):
    """Fetch issues from Jira and return count + formatted HTML list."""
    
    auth = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_TOKEN}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    url = f"{JIRA_URL}/rest/api/3/search/jql"
    payload = {
        "jql": jql,
        "maxResults": 50,
        "fields": ["summary", "key"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        issues = response.json().get("issues", [])

        # ✅ If no issues found
        if not issues:
            return 0, "<li>No issues found during this period.</li>"

        issue_list = ""

        for issue in issues:
            link = f"{JIRA_URL}/browse/{issue['key']}"
            summary = issue["fields"]["summary"]

            # Optional: add 🚨 emoji for Security issues
            if "Security" in summary:
                summary = f"🚨 {summary}"

            issue_list += f"""
                <li style="margin-bottom:6px;">
                    <a href="{link}" style="color:#0052CC; text-decoration:none; font-weight:bold;">
                        {issue['key']}
                    </a>
                    – {summary}
                </li>
            """

        return len(issues), issue_list

    except Exception as e:
        print(f"Error fetching Jira data: {e}")
        return 0, "<li>Error retrieving list.</li>"


def main():

    if not all([JIRA_EMAIL, JIRA_TOKEN, JIRA_URL, GMAIL_PASS]):
        print("Missing required environment variables.")
        return

    # Jira Queries
    count_created, list_created = get_issues(
        f"project={PROJECT_KEY} AND created >= -7d ORDER BY created DESC"
    )

    count_resolved, list_resolved = get_issues(
        f"project={PROJECT_KEY} AND resolved >= -7d ORDER BY resolved DESC"
    )

    count_open, list_open = get_issues(
        f"project={PROJECT_KEY} AND statusCategory != Done ORDER BY created DESC"
    )

    # Executive HTML Email Layout
    html_report = f"""
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, Helvetica, sans-serif;">

<table width="100%" bgcolor="#f4f6f8" cellpadding="0" cellspacing="0">
<tr>
<td align="center">

<table width="800" bgcolor="#ffffff" cellpadding="0" cellspacing="0" style="margin:30px 0;">

<tr>
<td bgcolor="#172B4D" style="padding:25px;">
<h2 style="color:#ffffff; margin:0;">
Jira Weekly Status Report – {PROJECT_KEY}
</h2>
<p style="color:#B3BAC5; margin:5px 0 0 0; font-size:13px;">
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
</p>
</td>
</tr>

<tr>
<td style="padding:25px;">

<h3 style="color:#172B4D;">Summary Stats</h3>
<ul>
<li><strong>Issues Created (Last 7 Days):</strong> {count_created}</li>
<li><strong>Issues Resolved (Last 7 Days):</strong> {count_resolved}</li>
<li><strong>Total Currently Open:</strong> {count_open}</li>
</ul>

<h3 style="color:#172B4D;">Created This Week</h3>
<ul>
{list_created}
</ul>

<h3 style="color:#172B4D;">Currently Open</h3>
<ul>
{list_open}
</ul>

</td>
</tr>

<tr>
<td bgcolor="#F4F5F7" style="padding:15px; text-align:center; font-size:12px; color:#6B778C;">
Automated Jira Executive Report
</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""

    # Send Email
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
