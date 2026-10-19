
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

from tools import *
from llm_provider import or_model,hf_model,google_model

system_prompt="""
You are search engine, you can extract,parse useful information from internet.
## capabilities:
    1.read file using `read_file'
    2.save file using 'save_file'
"""
custom_model=or_model

agent = create_agent(
        model=custom_model,
        tools=[read_file,save_file],
        system_prompt=system_prompt,
        middleware=[SummarizationMiddleware(custom_model,trigger=("fraction", 0.8),summarise=custom_model)],
        )
if __name__=="__main__":
    content="""
    I want you for each city entry in the file input.txt to:
    1.Retrieve its GPS coordinates, its country and the population count from the most recent census
    2.Save the output into output.txt
    """
    result = agent.invoke(
            {"messages": [{"role": "user", "content":content}]}
            )
    print(result["messages"][-1].content_blocks)

