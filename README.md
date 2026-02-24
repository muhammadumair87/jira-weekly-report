# 📊 Jira Weekly Executive Report Automation

Automated senior-level Jira reporting tool that generates a professional HTML email summary of project activity and sends it via Gmail.

This script is designed for IT Managers, Security Leads, and DevOps professionals who need structured weekly reporting directly from Jira.

---

## 🚀 Features

- Fetches Jira issues via REST API
- Generates executive-style HTML email report
- Clickable Jira ticket keys (no raw URLs)
- Weekly metrics:
  - Issues Created
  - Issues Resolved
  - Total Open Issues
- Secure environment variable handling
- Gmail SMTP integration
- Production-ready structure

---

## 🛠 Technologies Used

- Python 3
- Jira REST API v3
- Gmail SMTP (App Password)
- dotenv for secure configuration

---

## 📂 Project Structure

```
jira-weekly-report/
│
├── main.py
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/jira-weekly-report.git
cd jira-weekly-report
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and insert:

- Jira email
- Jira API token
- Jira URL
- Gmail App Password

---

## 🔐 Security Notes

- Never commit `.env` file
- Use Gmail App Password (not real password)
- Store Jira token securely
- Rotate API tokens periodically

---

## 📨 Example Output

The email includes:

- Executive summary
- Weekly metrics
- Clickable Jira ticket keys
- Professional HTML formatting

---

## ⏰ Cron Job Automation (Linux Example)

```bash
crontab -e
```

Add:

```bash
0 9 * * MON /usr/bin/python3 /path/to/main.py >> /path/to/log.txt 2>&1
```

Runs every Monday at 09:00.

---

## 📈 Future Improvements

- SLA breach detection
- Severity color coding
- Trend comparison (week-over-week)
- Embedded charts
- Microsoft Teams integration
- CI/CD pipeline integration

---

## 👤 Author

Muhammad Ahsan  
IT Automation & Security Enthusiast  
Berlin, Germany

---

## 📜 License

MIT License
