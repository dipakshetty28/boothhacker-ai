import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_booth_intel(company, search_data):
    context = "\n\n".join(
        [
            f"""
Title: {item.get('title')}

Snippet: {item.get('snippet')}

Link: {item.get('link')}
"""
            for item in search_data
        ]
    )

    prompt = f"""
You are an AI conference booth intelligence agent.

Company:
{company}

Research Data:
{context}

Generate a detailed report with:

1. What the company does
2. Recent company news
3. Interesting recent launches or announcements
4. Developer pain points
5. Best technical questions to ask
6. Networking conversation starters
7. Hiring/job opportunities
8. How a software engineer should pitch themselves
9. Should I apply? Score out of 10
10. Best conversation opener for this booth

Be practical, detailed, concise, and conference-focused.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content