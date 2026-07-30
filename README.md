Generative AI: Automated Copywriting & Tone Transformer

This project implements a CLI tool to compile a master instruction template and generate platform-specific marketing copy using an LLM.

Quickstart

1. Create a virtual environment and install deps:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

2. Set your OpenAI API key (do NOT commit your key):

Windows cmd:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

3. Run the CLI (example):

```bash
python run.py --product Shoe --name "Acme Runner" --tone witty --platform linkedin
```
"# Decode_lab_task_2 " 
