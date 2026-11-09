# from src.tools.tools import web_search,scrape_url
# output = web_search("Latest News on AI research")
# print(output)
#-------- when web_search is defined as @toop operation in tools.py so we should use it by "invoke"
# output = web_search.invoke("Latest News on AI research")
# output = scrape_url("https://www.sciencedaily.com/news/computers_math/artificial_intelligence")
# print(output)

from src.pipelines.pipeline import run_research_pipeline

topic = " The impact of AI on the job market in 2026"
run_research_pipeline(topic)
