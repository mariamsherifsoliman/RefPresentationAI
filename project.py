#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Imports 

import streamlit as st 
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import ArxivAPIWrapper
from langchain.tools import YouTubeSearchTool
from langchain.utilities import SerpAPIWrapper
from langchain.chains import SequentialChain
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
import os

# API keys 

openai_key = os.environ.get("OPENAI_API_KEY")

serpapi_key = os.environ.get("SERPAPI_API_KEY")

# LLM

llm = OpenAI(temperature=0.4) 

# App framework

st.title('RefPresentationAI: Your Reference-Rich Presentation Assistant🦜🔗 ')
prompt = st.text_input('Enter topic here') 

# Tools
  
ytb= YouTubeSearchTool()

arxiv = ArxivAPIWrapper()

search = SerpAPIWrapper()

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

Tool1=Tool(
    name = "Current Search",
    func=search.run,
    description="useful for when you need to explain topics"
)
Tool2=Tool(
    name = "Video Search",
    func=ytb.run,
    description="useful for when you need to give valid youtube links to videos that are educational and helpful about a certain topic"
    )
Tool3=Tool(
    name = "Wikipedia search",
    func=wikipedia.run,
    description="useful for when you need to give wikipedia page links that are educational and helpful about a certain topic"
    )
Tool4=Tool(
    name = "Arxiv search",
    func=arxiv.run,
    description="useful for when you need to give helpful refrences about a certain topic"
    )
tools = [
    Tool1,
    Tool3,
    Tool4
]

# Agent 

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


# Prompt templates

introprob_template=PromptTemplate(
    input_variables=["Topic",'Introduction'], 
    template="""
    You are a talented student, your job is to write a brief, informative introduction of an essay concerning {Topic} while using this research result: {Introduction}.
    After that, state a central question or challenge that you aim to address or explore; this question should set the stage for the presentation, guiding the audience's understanding of the topic.
    """
)

plan_template=PromptTemplate(
    input_variables=["Question"], 
    template="""
    Using this given introduction and central question: {Question}, create a plan for an essay with four parts. Part 1 should be the introduction, and Part 4 should be the conclusion. This plan should outline the main sections or points I should include in the essay to address the central question.
    """
)

body_template=PromptTemplate(
    input_variables=["Plan"], 
    template="""
    Using this essay plan: {Plan}, create the body for the second and third parts of the essay only. Answer the second and thrid sections outlined. For each section, you'll need write a couple of sentences that go along with the subsections.
    """
)

pred_template=PromptTemplate(
    input_variables=["Topic"], 
    template="""
    Predict a list of futur trends regarding this topic: {Topic}. State valid refrences to support your answer, leverage your answer using wikipedia pages, research papers and youtube videos 
    """
)

# Tool templates

ytb_template = PromptTemplate(
    input_variables = ['Topic', 'ytb'], 
    template='Recommend me helpful youtube video regarding this topic {Topic} while leveraging this youtube research:{ytb} '
)

paper_template = PromptTemplate(
    input_variables = ['Topic', 'arxiv'], 
    template='Recommend me helpful research papers regarding this topic {Topic} while leveraging this paper research:{arxiv} '
)

wiki_template = PromptTemplate(
    input_variables = ['Topic', 'wiki'], 
    template='Recommend me helpful wikipedia pages regarding this topic {Topic} while leveraging this wikipedia research:{wiki} '
)

# Chains

introprob_chain = LLMChain(llm=llm, prompt=introprob_template, verbose=True, output_key='Question')

plan_chain = LLMChain(llm=llm, prompt=plan_template, verbose=True, output_key='Plan')

dev_chain = LLMChain(llm=llm, prompt=body_template, verbose=True, output_key='Body')

ytb_chain = LLMChain(llm=llm, prompt=ytb_template, verbose=True, output_key='youtube')

paper_chain = LLMChain(llm=llm, prompt=paper_template, verbose=True, output_key='paper')

wiki_chain = LLMChain(llm=llm, prompt=wiki_template, verbose=True, output_key='wiki')

overall1_chain = SequentialChain(
    chains=[introprob_chain, plan_chain, dev_chain],
    input_variables=["Topic", "Introduction"],
    output_variables=["Question", "Plan","Body"],
    verbose=True)

# Output

if prompt: 

    dev=overall1_chain({"Topic":prompt, "Introduction":search.run(prompt)})
    st.write(dev)

    with st.expander('Trend Predictions'): 

        st.info(agent.run(pred_template.format(Topic=prompt)))

    with st.expander('Youtube References'): 

        ytb_research = ytb.run(prompt)
        st.info(ytb_research)
        #youtube = ytb_chain.run(Topic=prompt, ytb=clickable_links)
        

    with st.expander('Paper References'): 

        paper_research=arxiv.run(prompt)
        #paper = paper_chain.run(Topic=prompt, arxiv=paper_research)
        st.info(paper_research)

    with st.expander('Wikipedia References'): 

        wiki_research=wikipedia.run(prompt)
        #wiki = wiki_chain.run(Topic=prompt, wiki=wiki_research)
        st.info(wiki_research)

    



   




