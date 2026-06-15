from ai.tools import tools
from ai.checkpointer import create_checkpointer
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()


system_prompt = """
You are an Helpful AI personal assistant bot on telegram with the name 'Pilot AI'
Your username is 'task_pilot_imago_bot'.
"""

model = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="openai/gpt-oss-20b")
agent = create_agent(
    model, tools=tools, system_prompt=system_prompt, checkpointer=create_checkpointer()
)
