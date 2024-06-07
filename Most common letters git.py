import os
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import pandas as pd



os.environ['LANGCHAIN_API_KEY'] = 'langchain api key here'
    
os.environ['OPENAI_API_KEY'] = 'open ai api key here'

agent = create_csv_agent(
    ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-0125", max_tokens = 256),
    r'C:\Users\Usuario\Desktop\masters\Advanced topics deep learning\final paper\letter_position_wordle.csv',
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)


agent.invoke("From the list of five-letter words, please determine the most common letter for each position (first, second, third, fourth, and fifth) across all words.")
