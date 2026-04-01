# Julius Tex 🤖

> Interactive AI research assistant and LaTeX editor — right in your terminal.

Julius Tex reads your project's text files (`.tex`, `.bst`, `.cls`, `.bib`, `.md`, `.txt`, `.html`, `.xml`, `.json`, etc.),
a custom system prompt, and your API tokens, then starts an intelligent conversation
about your work.  Every question-and-answer pair is automatically saved as a
timestamped Markdown file and re-loaded the next time you run the tool, so the
assistant always has full context of previous sessions.

---

## Features

- 🤖 **Multiple AI providers** — Claude, Mistral, Perplexity, Grok, LM Studio, Ollama, GitHub Models, Azure AI Foundry, Alibaba Cloud, Zhipu AI (z.ai)
- 📄 **Automatic context loading** — reads all text files (`.tex`, `.md`, `.txt`, `.html`, `.xml`, etc.) in the current directory and its sub-directories
- 🧠 **Custom system prompt** — place a `PROMPT.sys` file in your project root
- 💾 **Persistent history** — each exchange is saved as `julius_YYYYMMDD_HHMMSS.md`
- ✨ **Beautiful TUI** — syntax-highlighted, streaming responses powered by [Rich](https://github.com/Textualize/rich)
- 🔌 **Extensible** — clean provider ABC makes adding new providers trivial

---

## Installation

You need python, pip and venv.
```bash
# 1 – Clone and install
git clone https://github.com/Escola-de-Matematica-Aplicada/julius-tex.git
cd julius-tex
python3.14 -m venv .venv3.14
source .venv3.14/bin/activate
pip install -e .
pip install -r requirements.txt

# 2 – Configure tokens
cp TOKENS.example TOKENS
$EDITOR TOKENS        # fill in at least one API key

# 3 – (Optional) add a system prompt to your project
cp PROMPT.sys.example PROMPT.sys
$EDITOR PROMPT.sys
```

> **Security note**: `TOKENS` is listed in `.gitignore` and will never be committed.

---

## Usage

Navigate to any project directory and run:

```bash
julius-tex
```

Julius Tex will:
1. Read all supported text files (`.tex`, `.md`, `.txt`, `.html`, `.xml`, etc.) in the current directory and its sub-directories as project context.
2. Read `PROMPT.sys` as the session system prompt (if present).
3. Read `TOKENS` for API keys (if present).
4. Start an interactive chat session.
5. Save each exchange as `julius_YYYYMMDD_HHMMSS.md` in the current directory.

### Slash commands

| Command | Description |
|---|---|
| `/help` | Show all available commands |
| `/quit` or `/exit` | Exit Julius Tex |
| `/clear` | Clear current session's message history |
| `/provider` | Show the active provider and model |
| `/providers` | List all configured providers and switch by number |
| `/models` | List available models for the active provider and optionally switch |
| `/context` | Show loaded context files |
| `/save` | Manually save the last exchange |

---

## Configuration

### `TOKENS` file

Copy `TOKENS.example` to `TOKENS` and fill in the keys you want to use.
The file format is simple `KEY=VALUE` pairs (lines starting with `#` are ignored):

```ini
ANTHROPIC_API_KEY=sk-ant-...
MISTRAL_API_KEY=...
PERPLEXITY_API_KEY=...
GROK_API_KEY=...
LMSTUDIO_URL=http://localhost:1234
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
GITHUB_TOKEN=ghp_...
AZURE_AI_FOUNDRY_ENDPOINT=https://your-resource.services.ai.azure.com/openai/v1/
AZURE_AI_FOUNDRY_API_KEY=...
DEFAULT_PROVIDER=claude
```

### `PROMPT.sys` file

Any text in this file becomes the system prompt for the entire session.
See `PROMPT.sys.example` for a starting template.

---

## Supported providers

| Provider | Token key | Notes |
|---|---|---|
| Anthropic Claude | `ANTHROPIC_API_KEY` | Default model: `claude-sonnet-4-5` |
| Minimax | `MINIMAX_API_KEY` | Anthropic-compatible API (text-anthropic) — list models with /models |
| Mistral AI | `MISTRAL_API_KEY` | Default model: `mistral-large-latest` |
| Perplexity | `PERPLEXITY_API_KEY` | Default model: `llama-3.1-sonar-large-128k-online` |
| Grok (xAI) | `GROK_API_KEY` | Default model: `grok-beta` |
| LM Studio | `LMSTUDIO_URL` | Local — OpenAI-compatible server |
| Ollama | `OLLAMA_URL` | Local — native Ollama API |
| GitHub Models | `GITHUB_TOKEN` | Default model: `openai/gpt-4o-mini` — [catalog](https://models.github.ai/catalog/models) |
| Azure AI Foundry | `AZURE_AI_FOUNDRY_API_KEY` + `AZURE_AI_FOUNDRY_ENDPOINT` | Default model: `gpt-4o` — [docs](https://ai.azure.com/) |
| Alibaba Cloud | `DASHSCOPE_API_KEY` | Default model: `qwen-max` — [docs](https://bailian.console.alibabacloud.com/) |
| Zhipu AI (z.ai) | `ZHIPU_API_KEY` | Default model: `glm-4` — [docs](https://open.bigmodel.cn/) |
| Google Gemini | `GEMINI_API_KEY` | Default model: `gemini-2.5-flash` — [docs](https://aistudio.google.com/) |

---

## Project layout

```
julius-tex/
├── julius_tex/
│   ├── __init__.py
│   ├── main.py          # CLI entry-point & chat loop
│   ├── config.py        # Load TOKENS, PROMPT.sys, plain-text files
│   ├── history.py       # Save/load conversation history
│   ├── ui.py            # Rich-based TUI components
│   └── providers/
│       ├── __init__.py          # Provider registry
│       ├── base.py              # BaseProvider ABC
│       ├── claude_provider.py   # Anthropic Claude
│       ├── mistral_provider.py  # Mistral AI
│       ├── openai_compat.py     # Perplexity, Grok, LM Studio, GitHub Models, Azure AI Foundry, Alibaba Cloud, Zhipu AI
│       └── ollama_provider.py   # Ollama
├── TOKENS.example       # Template — copy to TOKENS and fill in
├── PROMPT.sys.example   # Example system prompt
├── requirements.txt
└── pyproject.toml
```

---

## License

MIT — see [LICENSE](LICENSE) for details.
