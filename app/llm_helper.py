import requests
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

class OllamaClient:
    def __init__(self): 
        self.llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "gemma3n:latest") ,
            base_url=os.getenv("OLLAMA_HOST", "http://ollama-server:11434")
        ) 

    def generate(self, context, question):
        template = """
        You are an AI assistant. Strictly refuse to answer irrelevant questions. 
        Use the context below to answer the question. 
        Do not respond to irrelevant questions, except for the greetings.
        If the answer is not in the context, say 'Sorry, I can only answer based on this document.'
        Context:
        ---
        {context_}
        ---
        Question: {question_}
        Answer:
        """

        prompt = PromptTemplate.from_template(
            template = template.strip()
        )
        
        llm_chain = prompt | self.llm
        answer = llm_chain.invoke({"context_": context, "question_": question})
        return answer
