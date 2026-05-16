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
            f"Title: {item.get('title')}\n"
            f"Link: {item.get('link')}\n"
            f"Snippet: {item.get('snippet')}"
            for item in search_data
        ]
    )

    prompt = f"""
You are a conference booth intelligence agent.

Company: {company}

Search Context:
{context}

Generate:
1. What company does
2. Developer pain points
3. Smart booth questions
4. Resume/job fit
5. Should I apply?
6. 30-second networking pitch

Make it practical and concise.
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