# **Note** create_agent and create_react_agent are not similar both have similar porpuse but
# create_agent has become standard, streamlined function
# create_react_agent is older version
import os
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate # for preparing a custom prompt
from langchain_core.output_parsers import StrOutputParser#is used when you want to convert the output of an LLM into a normal Python string (str) instead of receiving a LangChain message object.
from src.tools.tools import web_search, scrape_url # these are from tools that we made
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#--------------
# Model Initialization
#--------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,     # Automatically retry up to 5 times on 503/429 errors
    google_api_key= GEMINI_API_KEY
)

# response = llm.invoke("Explain artificial intelligence in one sentence.")

# print(response.content)

#-------------
# Creating Agent
#-------------

def build_search_agent(): # First agent
    return create_agent(
        model= llm, 
        tools= [web_search]
        # system_prompt= if we want we can change this option
        )

def build_reader_agent(): # Second agent
    return create_agent(
        model= llm,
        tools= [scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()