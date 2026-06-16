from langchain_core.messages import HumanMessage
from telegram.ext import ContextTypes
from ai.agent import agent
from telegram import Update
from decorators import registered_only


@registered_only
async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text

    config = {
        "configurable": {
            "user_id": update.effective_user.id,
            "thread_id": f"telegram_{update.effective_user.id}",
        }
    }

    result = agent.invoke({"messages": [HumanMessage(content=prompt)]}, config=config)

    await update.message.reply_text(result["messages"][-1].content)
