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

# AI Tool Hunter MCP Server

Find the perfect AI tool for any task — directly from your IDE.

## What This Does
Exposes AI Tool Hunter's intelligent search as an MCP tool.
Ask your AI assistant to find tools and it calls this server live.

## Tools Available
- `hunt_ai_tool(query, category?)` — Find AI tools by use case
- `list_categories()` — See all available categories

## Connect to Claude Desktop
Add to your claude_desktop_config.json:
```json
{
  "mcpServers": {
    "ai-tool-hunter": {
      "url": "https://vishalclen-ai-tool-hunter-mcp.hf.space/gradio_api/mcp/sse"
    }
  }
}
```

## Connect to Cursor / VS Code
Add the SSE URL in MCP settings:
`https://vishalclen-ai-tool-hunter-mcp.hf.space/gradio_api/mcp/sse`

## Example Queries
- "Find me a free AI tool to generate images"
- "What's the best AI coding assistant?"
- "Find open source video generation tools"

Built by Vishal Singh
