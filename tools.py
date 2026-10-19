import subprocess
import urllib.error
import urllib.request

from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
@tool
def bash(command:str)-> str:
    """ Run shell command and return its combined stdout and stderr"""
    result=subprocess.run(command,shell=True,capture_output=True,text=True)
    return (result.stdout+result.stderr) or "no output"
@tool
def read_file(path:str)-> str:
    """ Read a file and return its content"""
    with open(path) as f:
        return f.read()
@tool
def save_file(path:str,content:str)-> None:
    """ write content into file """
    with open(path,'w') as f:
        return f.write(content)
@tool
def save_into_csv_file(path:str,content:str)-> None:
    """ write content into csv file """
    with open(path,'w') as f:
        return f.write(content)
@tool
def fetch_text_from_url(url: str) -> str:
    """Fetch the document from a URL.
    """
    req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
            )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    text = raw.decode("utf-8", errors="replace")
    return text
