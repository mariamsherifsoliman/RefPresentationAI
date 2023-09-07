# RefPresentationAI
Langchain python implementation, reference-rich presentation AI assistant. 

Project Objectives: 

Goal no 01: Automated Presentation Guide Generation
Develop an AI that can automatically generate a presentation guide based on a user input that consists of a certain topic or subject. The goal is to create a tool that generates key points that lead to a logical and put-together presentation.

Goal no 02: Accurate Refrence Generation
The AI should also incorperate relevant references from academic sources. Some of these sources include Youtube videos, research papers and so on...

Goal no 03: User Friendly
Create an intuitive and user-friendly design for RefPresentationAI that allows users to easily input topics. Additionally, provide helpful features like search history.

Expected Input: 
The user is expected to input the name of the topic / subject that they wish to get a presentation guide for.

Expected Output:
The desired output consists of a non-detailed structured presentation guide. Namely, the output should consist of a short introduction, a central question, a plan, the main points of the body, and predictions surrounding the topic. The output is expected to be short, straight to the point, and only containing a few sentences in each part. The agent is not meant to generate a whole presentation but a simple, yet informative guide supported by academic references.

Tools used:
-Agents 
-Chains, SequentialChains
-Prompt templates, prompt patterns
-Tools, youtube, arxiv, serpapi

To run: 
command "streamlit run {filename}.py"
