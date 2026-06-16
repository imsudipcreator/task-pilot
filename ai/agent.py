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

Don't respond complicated things to the user unless asked for. e.g., 
if users asks what tools do you use. Instead of telling the tools name, say what you can do with it.
Don't respond time's in a complicated way (e.g. 24:00). Respond in user friendly way (e.g. 12:00 AM).

Always respond in a human understandable way. keep responses short and straight to the point.
Use telegram formatting for bold, italic, etc.
Use telegram markdown for formatting.
"""

model = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="openai/gpt-oss-20b")
agent = create_agent(
    model, tools=tools, system_prompt=system_prompt, checkpointer=create_checkpointer()
)
