from mcp.server import FastMCP

import logging
from typing import Any


logger = logging.getLogger(__name__)


# Initialize MCPServer
mcp = FastMCP("test")

@mcp.tool()
def read_file(path:str)-> str:
    """ Read a file and return its content
    Args:
       path:the path to file to be read from 
    """
    with open(path) as f:
        return f.read()

@mcp.tool()
def save_file(path:str,content:str)-> None:
    """ write content into file 
    Args:
        path:The path to file to be written to
        content: the content to be written into the specified file
    """
    with open(path,'w') as f:
            f.write(content)

mcp.run(transport="stdio")
