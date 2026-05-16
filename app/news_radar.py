from serpapi_client import search_google


def get_live_news(company):
    queries = [
        f"{company} latest news",
        f"{company} AI announcement",
        f"{company} engineering blog",
        f"{company} GitHub",
        f"{company} release notes",
        f"{company} funding",
        f"{company} layoffs",
        f"{company} developer tools"
    ]

    all_results = []

    for query in queries:
        try:
            results = search_google(query, num=3)

            for item in results:
                all_results.append({
                    "query": query,
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", "")
                })

        except Exception as error:
            print(error)

    deduped = []
    seen = set()

    for item in all_results:
        link = item.get("link")

        if link and link not in seen:
            seen.add(link)
            deduped.append(item)

    return deduped[:12]