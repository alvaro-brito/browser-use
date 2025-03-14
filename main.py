import os
import re
import json
# Optional: Disable telemetry
# os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Optional: Set the OLLAMA host to a remote server
# os.environ["OLLAMA_HOST"] = "http://x.x.x.x:11434"
os.environ["OLLAMA_HOST"] = "https://kux579y5g3wu34-11434.proxy.runpod.net"

import asyncio
from browser_use import Agent
from browser_use.agent.views import AgentHistoryList
from langchain_ollama import ChatOllama

def extract_json_from_result(result):
    """
    Extract and parse JSON from the agent result.
    Handles JSON embedded in markdown code blocks and cleans it properly.
    """
    json_pattern = r"```json\s*([\s\S]*?)\s*```"
    json_matches = re.findall(json_pattern, str(result))
    
    if not json_matches:
        print("No JSON data found in code blocks, searching in raw text...")
        json_pattern = r"\{[\s\S]*?\}"
        json_matches = re.findall(json_pattern, str(result))
    
    if json_matches:
        json_text = json_matches[0]
        
        json_text = json_text.replace('\\n', '\n')
        json_text = json_text.replace('\\t', '\t')
        json_text = json_text.replace('\\r', '\r')
        
        json_text = json_text.strip()
        
        try:
            extracted_json = json.loads(json_text)
            print("\nSuccessfully extracted JSON:")
            print(json.dumps(extracted_json, indent=2, ensure_ascii=False))
            return extracted_json
        except json.JSONDecodeError as e:
            print(f"\nError parsing JSON: {e}")
            try:
                import ast
                normalized_text = json_text.replace("'", '"')
                python_dict = ast.literal_eval(normalized_text)
                return python_dict
            except Exception as e2:
                print(f"Failed final parsing attempt: {e2}")
                print("Returning partial data or empty dict")
                return {}
    else:
        print("No JSON data found in the result")
        return {}
    
    
async def run_search() -> AgentHistoryList:
    extend_system_message_custom = """
        REMEMBER the most important RULE:
        ALWAYS open first a new tab.
    """
    
    agent = Agent(
        task=f"""{extend_system_message_custom} Go to https://www.kayak.com.br/flights and search for 
                flights from Brasilia (type BSB and select the airport) to Orlando (type MCO and select the airport) leaving on April 1st and returning on April 15th. 
                when you have the list of fligts return the list of flights in a structured JSON""",
        llm=ChatOllama(
            model="deepseek-r1:32b",
            num_ctx=32000,
        )
    )

    result = await agent.run()
    extracted_json = extract_json_from_result(result)
    return extracted_json


async def main():
    result = await run_search()
    print("\n\n", result)


if __name__ == "__main__":
    asyncio.run(main())