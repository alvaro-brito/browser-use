# Browser Use with Ollama + DeepSeek R1

This project demonstrates how to use the `browser_use` package with Ollama and DeepSeek R1 models as an alternative to OpenAI's Operator feature. It allows AI models to browse the web and interact with websites autonomously.

## Overview

The `browser_use` package enables LLMs (Large Language Models) to control a web browser, allowing them to:
- Navigate to websites
- Fill out forms
- Click buttons
- Extract information
- Perform complex web-based tasks

This example specifically shows how to use DeepSeek R1 (via Ollama) to search for flights on Kayak Flights between Brasilia and Orlando for specific dates.

## Prerequisites

- Python 3.11+
- Ollama installed locally or access to a remote Ollama server
- DeepSeek R1 model downloaded in Ollama (specifically `deepseek-r1:32b`)
- Chrome or Chromium browser installed

## Quick Start

### Prepare the Environment

Browser Use requires Python 3.11 or higher.

1. **Set up Python environment with uv** (recommended):

```bash
uv venv --python 3.11
```

2. **Activate the virtual environment**:

```bash
# For Mac/Linux:
source .venv/bin/activate

# For Windows:
.venv\Scripts\activate
```

3. **Install dependencies**:

```bash
uv pip install browser-use
```

4. **Install Playwright** (required for browser automation):

```bash
playwright install
```

5. **Install additional packages for Ollama**:

```bash
uv pip install langchain_ollama
```

### Install Ollama (Optional)

If you want to use Ollama with local models:

- **macOS/Linux**: 
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **Windows**: Download from [Ollama's website](https://ollama.com/download)

Then pull the DeepSeek R1 model:

```bash
ollama pull deepseek-r1:32b
```

### Set up LLM API Keys

If using API-based LLMs like OpenAI or Anthropic, create a `.env` file with your API keys:

```
# .env file
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

For other LLM models, refer to the Langchain documentation for specific API key setup.

### Create an Agent

You can create an agent in two ways:

#### Option 1: Using OpenAI (GPT-4o)

Create a file named `agent.py`:

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

Run it with:

```bash
uv run agent.py
```

#### Option 2: Using Ollama with DeepSeek R1 (as shown in this repository)

Clone this repository:

```bash
git clone https://github.com/alvaro-brito/browser-use.git
cd browser-use-example
```

Run the example:

```bash
uv run main.py
```

## Configuration Options

The script includes several configuration options:

### Using a Remote Ollama Server

You can connect to a remote Ollama server by setting the `OLLAMA_HOST` environment variable:

```python
os.environ["OLLAMA_HOST"] = "http://your-server-address:11434"
```

### Disabling Telemetry

You can disable telemetry by uncommenting:

```python
# os.environ["ANONYMIZED_TELEMETRY"] = "false"
```

## Customizing the Task

To change what the agent does, modify the `task` parameter in the `Agent` constructor:

```python
agent = Agent(
    task="Your custom task description here",
    llm=ChatOllama(
        model="deepseek-r1:32b",
        num_ctx=32000,
    ),
)
```

## How It Works

1. The script initializes an `Agent` with a specific task and the DeepSeek R1 model via Ollama
2. The agent launches a browser and interprets the task
3. It navigates to Kayak Flights and performs the search
4. Results are returned as an `AgentHistoryList` object

## Advantages Over OpenAI's Operator

- **Open Source**: Works with open-source models like DeepSeek R1
- **Self-hosted**: Can run entirely on your own infrastructure
- **Customizable**: More flexibility in how the browser automation works
- **Cost-effective**: No API costs when running locally

## Limitations

- Requires more computational resources than API-based solutions
- Performance depends on the capabilities of the LLM being used
- May require fine-tuning for complex tasks
