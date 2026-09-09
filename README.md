# AI Code Agent

A lightweight AI coding agent built in Python using the OpenAI SDK and OpenRouter.

This project was built as part of the [Boot.dev](https://www.boot.dev/) AI Agent course to understand how AI coding agents work under the hood, including LLM integration, function calling, tool execution, and agent loops.

## Features

*  AI-powered coding assistant
*  Agent loop with iterative tool execution
*  Function calling with structured tool schemas
*  Safe file system operations
*  Python file execution
*  Calculator application
*  Command-line interface
*  Optional verbose output with token usage
*  Working-directory restrictions for file operations
*  Automated tests for agent tools

## Available Tools

The agent currently supports four main tools:

### `get_files_info`

Lists files and directories inside the permitted working directory.

Example:

```text
use get_files_info to list the files in the working directory
```

### `get_file_content`

Reads the contents of a file.

Files larger than 10,000 characters are automatically truncated.

Example:

```text
use get_file_content to get the contents of lorem.txt
```

### `write_file`

Creates or updates a file inside the permitted working directory.

Example:

```text
use write_file to create a new README.md file
```

### `run_python_file`

Executes a Python file and returns its output.

Example:

```text
use run_python_file to run tests.py
```

## How It Works

The agent follows a simple tool-calling loop:

```text
User Prompt
     │
     ▼
   LLM
     │
     ├── Normal response ──────► Return response
     │
     └── Tool call
             │
             ▼
        Execute tool
             │
             ▼
       Return tool result
             │
             ▼
            LLM
             │
             └──────► Continue until task is complete
```

The model receives the available function schemas and can decide when a tool is required to complete the user's request.

## Project Structure

```text
.
├── calculator/
│   ├── main.py
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
│
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
│
├── call_function.py
├── main.py
├── prompts.py
│
├── test_get_files_info.py
├── test_get_file_content.py
├── test_write_file.py
├── test_run_python_file.py
│
├── pyproject.toml
├── uv.lock
└── README.md
```

## Tech Stack

* **Python**
* **OpenAI Python SDK**
* **OpenRouter**
* **uv** - Python package and project management
* **python-dotenv**
* **pytest**
* **Git**

## Requirements

* Python 3.10+
* [uv](https://docs.astral.sh/uv/)
* An OpenRouter API key

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/adm22222/ai-agent.git
cd ai-agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure the API key

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

> Never commit your `.env` file or expose your API key publicly.

## Usage

Run the agent with a prompt:

```bash
uv run main.py "How does the calculator render results to the console?"
```

Enable verbose output:

```bash
uv run main.py "use get_files_info to list the files in the working directory" --verbose
```

The `--verbose` option displays additional information such as token usage.

## Testing

Run the test suite with:

```bash
uv run pytest
```

You can also test the agent manually with prompts such as:

```bash
uv run main.py "use get_files_info to list the files in the working directory" --verbose
```

```bash
uv run main.py "use get_file_content to get the contents of lorem.txt" --verbose
```

```bash
uv run main.py "use write_file to create a new test.txt file with the contents 'hello'" --verbose
```

```bash
uv run main.py "use run_python_file to run tests.py" --verbose
```

## Path Safety

File-system tools are restricted to the configured working directory.

Path resolution and validation are centralized in:

```text
functions/path_utils.py
```

This prevents tools from accessing files outside the permitted working directory through paths such as:

```text
../some-file
```

## What I Learned

Building this project helped me understand how AI coding agents are structured beyond simply sending prompts to an LLM.

Key concepts covered:

* Integrating an LLM through an API
* System prompts and agent instructions
* Function/tool schemas
* Function calling
* Parsing tool arguments
* Executing tools dynamically
* Building an agent loop
* Passing tool results back to the model
* File-system safety
* Token usage tracking
* Error handling
* Writing tests
* Refactoring shared functionality
* Managing a project with Git

## Security Notice

This project is intended for learning purposes.

The agent has access to file-system operations and can execute Python code. It should **not** be treated as a production-grade or fully secure coding agent.

Do not run it in an environment containing sensitive files or credentials.

## Disclaimer

This is an educational project created while learning how AI agents and tool-calling systems work.

It is intentionally lightweight and focuses on understanding the core concepts behind AI coding agents rather than providing a production-ready coding assistant.
