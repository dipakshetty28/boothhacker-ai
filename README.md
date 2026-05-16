# BoothHacker AI 🎯

BoothHacker AI is an MCP-powered conference intelligence agent built using SerpApi, Streamlit, and AI.

The app helps developers attending conferences like PyCon US:
- verify whether a company has a booth
- find booth assignment information
- discover software engineering jobs
- analyze company news and engineering activity
- generate networking questions and booth strategy

---

# Features

## ✅ PyCon US 2026 Booth Validator
Checks whether the entered organization exists in the official PyCon US 2026 booth assignment sheet.

## ✅ Booth Assignment Lookup
Finds matching booth assignment rows and floorplan references.

## ✅ Live Booth News Radar
Uses SerpApi to search:
- latest company news
- AI launches
- engineering blogs
- GitHub activity
- funding announcements
- hiring trends

## ✅ Software Engineering Job Discovery
Finds up to 5 relevant software engineering-related jobs using SerpApi search.

## ✅ AI Booth Intelligence Report
Generates:
- company summary
- technical questions to ask
- networking conversation starters
- likely engineering pain points
- hiring insights
- resume/job fit analysis
- conference strategy

## ✅ SerpApi MCP Workflow
The project is designed around an MCP-style agent workflow:
- Booth Validation Agent
- Search Agent
- Job Discovery Agent
- News Radar Agent
- AI Strategy Agent

---

# Tech Stack

- Python
- Streamlit
- SerpApi Search API
- SerpApi MCP
- OpenAI API
- BeautifulSoup
- Requests

---

# Setup Instructions

Follow these steps to run BoothHacker AI locally and deploy it using Streamlit Cloud.

### Prerequisites

Install:
- Python 3.10+
- Git

Create a free SerpApi account:
https://serpapi.com/users/sign_up

Get your SerpApi API key:
https://serpapi.com/manage-api-key

You will also need an OpenAI API key.

### Clone Repository

```bash
git clone https://github.com/dipakshetty28/boothhacker-ai.git
cd boothhacker-ai
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
SERPAPI_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Do NOT commit `.env` to GitHub.

### Run Application

```bash
streamlit run app/main.py
```

Application will start at:

```txt
http://localhost:8501
```

## How the App Works

1. User enters a company or organization name
2. App validates whether the organization exists in the official PyCon US 2026 booth assignment sheet
3. If organization exists:
   - retrieves booth assignment information
   - searches latest company news
   - searches software engineering jobs
   - discovers engineering activity
   - generates booth networking strategy using AI
4. User receives:
   - booth assignment info
   - Live Booth News Radar
   - software engineering jobs
   - AI-generated booth intelligence report