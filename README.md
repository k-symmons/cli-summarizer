# CLI Summarizer

A Python CLI tool that summarizes text using the OpenAI API.

## Installation

```bash
pip install -e .
```

Or with pipx (recommended — installs in an isolated environment):

```bash
pipx install .
```

## Setup

Run this once to save your API key:

```bash
cli-summarizer -key YOUR_API_KEY
```

Your key is saved to `~/.config/cli-summarizer/.env` and will be loaded automatically on every run, no matter where you are in your terminal.

**Power user tip:** If you already have `OPENAI_API_KEY` set in your shell (e.g. `.zshrc`), the tool will use that automatically — no setup needed.

## Usage

Summarize a file:
```bash
cli-summarizer <file_path>
```

Summarize direct text:
```bash
cli-summarizer -t "your text here"
```

Set your API key and summarize in one command:
```bash
cli-summarizer -key YOUR_API_KEY -t "your text here"
```

## Requirements

- Python 3.8+
- OpenAI API key

## Platform Support

Currently macOS and Linux only. Happy to merge fixes for Windows!
