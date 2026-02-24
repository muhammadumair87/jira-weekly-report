# 📊 Jira Weekly Executive Report Automation

Automated senior-level Jira reporting tool that generates a professional HTML email summary of project activity and sends it via Gmail.

This project is designed for IT Managers, Security Leads, and DevOps professionals who need structured weekly reporting directly from Jira.

---

## 🚀 Features

- ✅ Connects securely to Jira Cloud API
- ✅ Fetches:
  - Issues Created (Last 7 Days)
  - Issues Resolved (Last 7 Days)
  - Currently Open Issues
- ✅ Generates executive-style HTML email
- ✅ Sends report via Gmail SMTP
- ✅ Fully automated with GitHub Actions
- ✅ Secure secrets management (no credentials stored in repo)
- ✅ Weekly scheduled execution

---

## 📸 Sample Report Output

The email includes:

- Executive header section
- Summary statistics
- Created This Week section
- Currently Open issues section
- Clickable Jira issue links
- Professional HTML layout

---

## 🏗 Project Structure

jira-weekly-report/
│
├── main.py # Core Jira report script
├── requirements.txt # Python dependencies
├── .github/
│ └── workflows/
│ └── jira-report.yml # GitHub Actions workflow
├── .gitignore
└── README.md



---

## 🔐 Required Secrets (GitHub Actions)

Add the following secrets in:

**Repository → Settings → Secrets → Actions**

| Secret Name | Description |
|------------|-------------|
| `JIRA_EMAIL` | Your Jira account email |
| `JIRA_TOKEN` | Jira API token |
| `JIRA_URL` | Your Jira base URL (e.g. https://yourcompany.atlassian.net) |
| `GMAIL_PASS` | Gmail App Password (16-character app password) |

⚠ Do NOT include `JIRA_EMAIL=` inside the secret value.  
Only paste the raw value.

---

## ⚙️ GitHub Actions Workflow

The workflow automatically runs:

- Every Monday (scheduled)
- Or manually via "Run workflow"

Example cron configuration:

```yaml
on:
  schedule:
    - cron: '0 10 * * 1'   # Every Monday 10:00 UTC
  workflow_dispatch:

🐍 Local Development Setup

Clone repository

git clone https://github.com/yourusername/jira-weekly-report.git
cd jira-weekly-report

Install dependencies

pip install -r requirements.txt

Create .env file (for local testing only)

JIRA_EMAIL=your_email
JIRA_TOKEN=your_token
JIRA_URL=https://yourcompany.atlassian.net
GMAIL_PASS=your_gmail_app_password

Run locally
python main.py

📧 Gmail Setup

To use Gmail SMTP:

Enable 2-Step Verification

Generate App Password

Use the 16-character app password as GMAIL_PASS

SMTP configuration used:

smtp.gmail.com
Port: 465 (SSL)

🔄 How It Works

GitHub Action starts

Python environment is prepared

Secrets injected as environment variables

Script calls Jira REST API

HTML report is generated

Email is sent securely via Gmail

Workflow completes

Technologies Used

Python 3

Jira Cloud REST API

Requests library

SMTP (Gmail SSL)

GitHub Actions (CI/CD)

HTML email templating

Environment variable security

Future Improvements (Optional)

PDF attachment export

CSV issue export

Slack notification integration

Confluence page publishing

Multi-project support

Executive KPI dashboard metrics

🛡 Security Notes

No credentials stored in repository

All secrets managed via GitHub Actions

.env excluded via .gitignore

SMTP uses SSL encryption
