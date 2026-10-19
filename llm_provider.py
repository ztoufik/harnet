from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv("api_keys.txt")
or_model = ChatOpenAI(
        model="nvidia/nemotron-3.5-super-vl",
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url=os.environ["OPENROUTER_BASE_URL"],
        max_tokens=4096,
        profile={"max_input_tokens":31949} 
        )
hf_model = ChatOpenAI(
        model="XiaomiMiMo/MiMo-V2.6-Pro-RL:novita",
        api_key=os.environ["HF_API_KEY"],
        base_url=os.environ["HF_BASE_URL"],
        profile={"max_input_tokens":262144} 
        )
google_model = ChatOpenAI(
        model="gemini-2.5-flash-lite",
        api_key=os.environ["GOOGLE_API_KEY"],
        base_url=os.environ["GOOGLE_BASE_URL"],
        )
