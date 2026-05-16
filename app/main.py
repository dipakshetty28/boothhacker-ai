import os
import streamlit as st
from dotenv import load_dotenv

from serpapi_client import search_google
from agent import generate_booth_intel
from pycon_booth import find_org_booth
from news_radar import get_live_news

load_dotenv()

st.set_page_config(
    page_title="BoothHacker AI",
    page_icon="🎯",
    layout="wide"
)

st.title("BoothHacker AI")
st.caption("Check PyCon US 2026 booth presence, find jobs, and generate booth strategy using SerpApi + AI")

with st.sidebar:
    st.header("Configuration Check")

    if os.getenv("SERPAPI_KEY"):
        st.success("SERPAPI_KEY loaded")
    else:
        st.error("SERPAPI_KEY missing")

    if os.getenv("OPENAI_API_KEY"):
        st.success("OPENAI_API_KEY loaded")
    else:
        st.error("OPENAI_API_KEY missing")

company = st.text_input(
    "Enter company or organization name",
    placeholder="Example: SerpApi"
)

generate_button = st.button("Generate Booth Intel", type="primary")

if generate_button:
    if not company.strip():
        st.warning("Please enter a company or organization name.")
        st.stop()

    if not os.getenv("SERPAPI_KEY"):
        st.error("SERPAPI_KEY is missing. Add it to your .env file.")
        st.stop()

    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is missing. Add it to your .env file.")
        st.stop()

    company = company.strip()

    st.markdown("---")

    with st.spinner("Checking PyCon US 2026 booth assignment sheet..."):
        booth_info = find_org_booth(company)

    st.subheader("PyCon US 2026 Booth Check")

    if not booth_info.get("found"):
        st.error(f"{company} is not present in the PyCon US 2026 booth assignment sheet.")

        if booth_info.get("floorplan_url"):
            st.link_button("Open PyCon Floor Plan", booth_info["floorplan_url"])

        if booth_info.get("sheet_url"):
            st.link_button("Open Booth Assignment Sheet", booth_info["sheet_url"])

        st.info("Research stopped because this app only generates booth intelligence for organizations present at PyCon US 2026.")
        st.stop()

    st.success(f"{company} is present in the PyCon US 2026 booth assignment sheet.")

    matches = booth_info.get("matches", [])

    booth_context = ""
    if matches:
        st.write("Matching booth assignment rows:")
        for row in matches:
            st.code(row)
        booth_context = "\n".join(matches)

    col1, col2 = st.columns(2)

    with col1:
        if booth_info.get("floorplan_url"):
            st.link_button("Open PyCon Floor Plan", booth_info["floorplan_url"])

    with col2:
        if booth_info.get("sheet_url"):
            st.link_button("Open Booth Assignment Sheet", booth_info["sheet_url"])

    st.markdown("---")

    with st.spinner("Finding software engineering jobs using SerpApi..."):
        job_queries = [
            f"{company} software engineer jobs",
            f"{company} careers software engineer",
            f"{company} backend engineer jobs",
            f"{company} full stack engineer jobs",
            f"{company} developer advocate jobs"
        ]

        job_results = []

        for query in job_queries:
            try:
                results = search_google(query, num=3)
                for item in results:
                    title = item.get("title", "").lower()
                    snippet = item.get("snippet", "").lower()

                    if any(
                        keyword in title or keyword in snippet
                        for keyword in [
                            "software engineer",
                            "backend engineer",
                            "frontend engineer",
                            "full stack",
                            "developer advocate",
                            "developer relations",
                            "python engineer",
                            "platform engineer"
                        ]
                    ):
                        job_results.append(item)

            except Exception as error:
                st.warning(f"Job search failed for query: {query}")
                st.caption(str(error))

        deduped_jobs = []
        seen_links = set()

        for job in job_results:
            link = job.get("link")
            if link and link not in seen_links:
                seen_links.add(link)
                deduped_jobs.append(job)

        top_jobs = deduped_jobs[:5]

    st.subheader("Software Engineering Related Jobs")

    if top_jobs:
        for index, job in enumerate(top_jobs, start=1):
            st.markdown(f"### {index}. {job.get('title', 'Untitled Job')}")
            st.write(job.get("snippet", "No description available."))
            if job.get("link"):
                st.link_button("Open Job Link", job["link"])
    else:
        st.info("No software engineering related jobs found from SerpApi search.")

    st.markdown("---")

    with st.spinner("Generating Live Booth News Radar..."):
        live_news = get_live_news(company)

    st.subheader("🚨 Live Booth News Radar")

    if live_news:
        for news in live_news[:8]:
            st.markdown(f"### {news.get('title')}")

            st.write(news.get("snippet"))

            if news.get("link"):
                st.link_button(
                    "Open Article",
                    news.get("link")
                )

            st.caption(f"Source Query: {news.get('query')}")
            st.markdown("---")
    else:
        st.info("No recent news found.")

    with st.spinner("Searching company intelligence with SerpApi..."):
        research_queries = [
            f"{company} company official website",
            f"{company} GitHub",
            f"{company} API developer pain points",
            f"{company} competitors",
            f"{company} recent news developer tools"
        ]

        all_results = []

        for query in research_queries:
            try:
                results = search_google(query, num=3)
                all_results.extend(results)
            except Exception as error:
                st.warning(f"Research search failed for query: {query}")
                st.caption(str(error))

    all_results.insert(
        0,
        {
            "title": "PyCon US 2026 Booth Assignment",
            "link": booth_info.get("sheet_url", ""),
            "snippet": booth_context
        }
    )

    for job in top_jobs:
        all_results.append(
            {
                "title": f"Software Engineering Job: {job.get('title', '')}",
                "link": job.get("link", ""),
                "snippet": job.get("snippet", "")
            }
        )
    
    for news in live_news:
        all_results.append(
            {
                "title": f"News: {news.get('title')}",
                "link": news.get("link"),
                "snippet": news.get("snippet")
            }
        )

    with st.spinner("Generating booth strategy..."):
        try:
            report = generate_booth_intel(company, all_results)
        except Exception as error:
            st.error("Failed to generate AI report.")
            st.exception(error)
            st.stop()

    st.subheader("Booth Intelligence Report")
    st.markdown(report)

    st.download_button(
        label="Download Report",
        data=report,
        file_name=f"{company.lower().replace(' ', '_')}_booth_intel.md",
        mime="text/markdown"
    )

    with st.expander("Raw SerpApi Search Results"):
        for item in all_results:
            st.markdown(f"**{item.get('title', 'Untitled')}**")
            st.write(item.get("snippet", "No snippet available."))
            if item.get("link"):
                st.write(item.get("link"))
            st.markdown("---")