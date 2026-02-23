# Offline Code Assistant (Ollama + Qwen3-Coder)

A lightweight local code assistant built with Python and Ollama.  
This tool allows you to load local project files, analyze them, and generate modified versions using a local large language model such as `qwen3-coder`.

It runs entirely offline and can be executed directly inside PyCharm.

---

## Features

- Load single files or entire folders
- Analyze Python projects
- Generate full modified file content
- Safe preview mode (no file overwrite unless confirmed)
- Works fully offline with Ollama
- Designed for Flask and general Python projects

---

## Requirements

- Python 3.9+
- Ollama installed on Windows
- A downloaded model, for example:

```bash
ollama pull qwen3-coder:30b
```

If memory is limited, use a quantized version such as:
```bash
ollama pull qwen3-coder:30b-a3b-q4_K_M
```
---
## Installation

1.Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/offline-code-assistant.git
cd offline-code-assistant
```

2.Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```
3.Install dependencies:
```bash
pip install -r requirements.txt
Project Structure
offline_code_assistant/
  main.py
  assistant.py
  file_context.py
  patch_parser.py
  requirements.txt
```  
## Usage

### Start the assistant
```bash
python main.py
```
You will see:
```bash
离线代码助手启动
模型: qwen3-coder:30b
num_ctx: 8192
```
---
### Load a file
```bash
load path/to/your/file.py
```

Example:

```bash
load C:\Users\username\PycharmProjects\BUS\app\model.py
```
### Analyze a file
```bash
ask Explain what this file does. Do not modify the code.
```

### Generate modified code
```bash
ask Add created_at and updated_at fields to this model and output the full updated file.
```
The assistant will return:
- A summary
- A full modified file inside a [PATCH] block
- Notes explaining changes

---
### Preview changes
```bash
show
```

### Apply changes (optional)

If you want to overwrite the file:
```bash
apply
```
You must type:
```bash
YES
```
to confirm.

If you do not run apply, your files remain unchanged.

---
Environment Variables (Optional)

You can control the model and context length:
```bash
set OFFLINE_MODEL=qwen3-coder:30b
set OFFLINE_NUM_CTX=4096
set OFFLINE_TEMPERATURE=0.15
```

---

## Recommended Settings

For a machine with 32GB RAM and 8GB VRAM:

- Model: qwen3-coder:30b

- num_ctx: 4096 or 8192

- temperature: 0.1 to 0.2、

---

## Safety Notes

- Always review generated code before applying.

- Avoid loading large folders such as .venv, .git, or node_modules.

- Prefer loading only relevant files for better results.

## Example Workflow
```bash
load app/models.py
ask Add a role field with default "student" and output the full updated file.
show
apply
```

## License

MIT License

You are free to modify and redistribute this project.

---

## Author

Hao Ni

University of Birmingham

925884246nh@gmail.com
