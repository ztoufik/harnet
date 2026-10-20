import asyncio

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools

from tools import *
from llm_provider import or_model,hf_model,google_model

system_prompt="""
You are search engine, you can extract,parse useful information from internet.
## capabilities:
    1.read file using `read_file'
    2.save file using 'save_file'
"""
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
            I want you for each city entry in the file input.txt to:
            1.Retrieve its GPS coordinates, its country and the population count from the most recent census
            2.Save the output into output.txt
            """
            result = await agent.ainvoke( {"messages": [{"role": "user", "content":content}]})
            return result["messages"][-1].content_blocks


if __name__=="__main__":
    result=asyncio.run(main())
    print(result)
