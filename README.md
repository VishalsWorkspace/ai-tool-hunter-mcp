---
title: AI Tool Hunter MCP
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.28.0
app_file: app.py
pinned: false
license: mit
---

# 🔍 AI Tool Hunter MCP

[![Live on Render](https://img.shields.io/badge/Live-Render-46E3B7?logo=render&logoColor=white)](https://ai-tool-hunter-mcp.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-5.28-F97316?logo=gradio&logoColor=white)](https://www.gradio.app/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-6366F1)](https://modelcontextprotocol.io/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What it does

Finds the right AI tool for any task, live, and hands it back as structured JSON your IDE or agent can use directly. No stale directories, no sponsored "Top 10" listicles — just real product pages, pricing, and a reason it fits.

## How it works

- **Tavily** runs an advanced live web search scoped to official product pages — pricing and feature terms baked into the query, directory/listicle domains excluded.
- **Groq** (`llama-3.3-70b-versatile`) reads the raw search results and extracts real tools, discarding blogs, newsletters, and "Top 10" round-ups.
- The result ships back as **clean, structured JSON** — no markdown, no prose, ready to render or pipe straight into another tool call.

## Tools exposed

| Tool | Parameters | Returns |
|---|---|---|
| `hunt_ai_tool` | `query: str` — what you want to do (e.g. `"generate images from text"`)  `category: str = "ALL"` — one of `ALL, CODING, WRITING, DESIGN, VIDEO, AUDIO, BUSINESS, RESEARCH` | JSON array of tools: `name`, `description`, `url`, `pricing`, `category`, `why_it_fits` |
| `list_categories` | *(none)* | JSON array of all valid category filters |

## Connect via MCP

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ai-tool-hunter": {
      "url": "https://ai-tool-hunter-mcp.onrender.com/gradio_api/mcp/sse"
    }
  }
}
```

**Cursor / VS Code** — add the same SSE URL in your MCP settings:

```
https://ai-tool-hunter-mcp.onrender.com/gradio_api/mcp/sse
```

## Example queries

- "Find me a free AI tool to generate images from text"
- "What's the best AI coding assistant for a Python monorepo?"
- "Find open source video generation tools"
- "I need something to transcribe and summarize podcasts"
- "Best AI tool for turning a rough outline into slides"

## Tech stack

[![Gradio](https://img.shields.io/badge/Gradio-UI%20%2B%20MCP%20server-F97316?logo=gradio&logoColor=white)](https://www.gradio.app/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036)](https://groq.com/)
[![Tavily](https://img.shields.io/badge/Tavily-Search%20API-1E293B)](https://tavily.com/)
[![httpx](https://img.shields.io/badge/httpx-async%20client-0A9EDC)](https://www.python-httpx.org/)

---

Built by **Vishal Singh**
