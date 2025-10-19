🧠 LangGraph Assistant

An AI assistant built with Python, LangGraph, and LangChain, using uv for environment and dependency management.

⚙️ 1. Environment setup

Create a .env file in the project root with your OpenAI API key:

```bash
OPENAI_API_KEY="your_api_key_here"
```

🧰 2. Create and activate the virtual environment

If you’re using uv (recommended):

```bash
uv venv
source .venv/bin/activate
```

If you don’t have uv yet:
```bash
pip install uv
```

📦 3. Install dependencies
```bash
make install
```
This will install all dependencies listed in pyproject.toml.
