from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Literal
from ddgs import DDGS


class WebSearchSchema(BaseModel):
    query: str = Field(..., description="The query to search for")
    type: Literal["text", "image", "video", "news"] = Field(
        "text", description="The type of content to search for"
    )
    max_results: int = Field(5, description="The maximum number of results to return")


@tool
def web_search(input: WebSearchSchema):
    """
    Use this tool to search the web. It is very versatile, Use smartly.
    This can provide videos, images, texts and even news with relevant info and sources depending on what type you want.
    """
    print(
        f"[TOOL_CALLED] web_search with query: {input.query}, type: {input.type}, max_results: {input.max_results}"
    )

    match input.type:
        case "image":
            results = DDGS().images(query=input.query, max_results=input.max_results)
            formatted = "\n\n".join(
                f"🔹 {r['title']}\n{r['image']}\n{r['source']}" for r in results
            )

            return formatted
        case "news":
            results = DDGS().news(query=input.query, max_results=input.max_results)
            formatted = "\n\n".join(
                f"🔹 {r['title']}\n{r['date']}\n{r['body']}\n{r['url']}"
                for r in results
            )

            return formatted
        case "video":
            results = DDGS().videos(query=input.query, max_results=input.max_results)
            formatted = "\n\n".join(
                f"🔹 {r['title']}\n{r['content']}\n{r['publisher']}" for r in results
            )

            return formatted
        case "text" | _:
            results = DDGS().text(query=input.query, max_results=input.max_results)
            formatted = "\n\n".join(
                f"🔹 {r['title']}\n{r['href']}\n{r['body']}" for r in results
            )

            return formatted
