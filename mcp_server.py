import logging
from typing import Any

from mcp.server import MCPServer

logger = logging.getLogger(__name__)


# Initialize MCPServer
mcp = MCPServer("test")

@mcp.tool()
async def read_file(path:str)-> str:
    """ Read a file and return its content
    Args:
       path:the path to file to be read from 
    """
    async with open(path) as f:
        return f.read()

@mcp.tool()
async def save_file(path:str,content:str)-> None:
    """ write content into file 
    Args:
        path:The path to file to be written to
        content: the content to be written into the specified file
    """
    async with open(path,'w') as f:
            f.write(content)

if __name__ == "__main__":
    mcp.run(transport="stdio")
