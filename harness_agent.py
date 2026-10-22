import asyncio

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

from tools import *
from llm_provider import or_model,hf_model,google_model

skills=[
        {"name":"python programmer","description":"python programming expertise that can craft task specific python scripts respecting PEP coding guidlines"}
        ]

system_prompt="""
You are search engine, you can extract,parse useful information from internet.
## capabilities:
    1.read file using `read_file'
    2.save file using 'save_file'
    3.load skill markdown file using 'load_skill'
## Skills:

""" +"".join(f'{i}.s["name"]' for i,s in enumerate(skills))

custom_model=or_model

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["mcp_server.py"],
)

mcp_tools=[]

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            mcp_tools = await load_mcp_tools(session)
            agent = create_agent(
                    model=custom_model,
                    tools=mcp_tools,
                    system_prompt=system_prompt,
                    middleware=[SummarizationMiddleware(custom_model,trigger=("fraction", 0.8),summarise=custom_model)],
                    )
            content="""
             1.Use `python programmer` skill if necessary
             2.Craft python program that parse pdf file using PyMuPdf library and construct table of its contents.
             3.Save the script into loca python file using `write_file`tool with an appropriate name.
            """
            result = await agent.ainvoke( {"messages": [{"role": "user", "content":content}]})
            #return result["messages"][-1].content_blocks
            return result


if __name__=="__main__":
    result=asyncio.run(main())
    for message in result["messages"]:
        if hasattr(message, 'pretty_print'):
            message.pretty_print()
        else:
            print(f"{message.type}: {message.content}")
